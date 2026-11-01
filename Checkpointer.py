import os
import dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver
from langchain.agents.middleware import SummarizationMiddleware


dotenv.load_dotenv()

class Agent:
    def __init__(self, checkpointer):

        self.llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.5)

        self.agent = create_agent(
            model=self.llm,
            system_prompt='Give short answers',
            tools=[],
            checkpointer=checkpointer,
            middleware=[SummarizationMiddleware(
                model= self.llm, 
                max_tokens_before_summary=500,
                messages_to_keep=5,
            )]
        )

    def chat_loop(self):
        active_session = 'session_1'
        while True:
            user_input = input(
                'ask something (type "q" to terminarte, type "ch" to change session) :').strip().lower()
            
            if user_input == 'q':
                print('good luck')
                break

            if user_input == 'ch':
                active_session = 'session_2' if active_session == 'session_1' else 'session_1'
                print('Done.')
                continue

            config = {'configurable': {'thread_id': active_session}}
            response = self.agent.invoke({'messages': HumanMessage(user_input)}, config)

            print(response['messages'][-1].content)

        messages_config = {'configurable': {'thread_id': active_session}}
        state = self.agent.get_state(messages_config)
        print(state.values['messages'])

        

        
def main():
    db_uri = os.environ['DATABASE_URL']

    with PostgresSaver.from_conn_string(db_uri) as checkpointer: 
        checkpointer.setup()
        agent = Agent(checkpointer)
        agent.chat_loop()

if __name__ == '__main__':
    main()