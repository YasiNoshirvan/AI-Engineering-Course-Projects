import os
import dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field


dotenv.load_dotenv()

class User(BaseModel):
   name :str = Field(description='the name of the user : ')
   age: int = Field(description='the age of the user : ')
   companies: list[str] = Field(description='the companies associated with the user : ')
   net_worth : str = Field(description='the net worth of the user : ')


class Agent:
    def __init__(self):
        self.llm = ChatGroq(model = 'openai/gpt-oss-20b' , temperature=0.1)

    
    def Chat(self):

      '''
      history = [HumanMessage('I am tired'),
                 AIMessage('>>>sono stanco<<<'),
                 HumanMessage('I hate you'),
                 AIMessage('>>>ti odio<<<')]

      prompt = ChatPromptTemplate.from_messages([
         ('system' , 'You are a translator from {origin} to {to}'),
         MessagesPlaceholder(variable_name='history_variable'),
         ('human','{input}')

      ])

      #print(prompt.format_messages(origin='English' , to = 'German' , input = 'I love you'))

      chain = prompt | self.llm 

      response = chain.invoke({
    'history_variable': history,
    'origin': 'English',
    'to': 'Italian',
    'input': 'I am tired'
    })
      print(response.content)
   '''
      
      user_schema = {
          "title": "User",
          "type": "object",
          "properties": {
              "name": {"type": "string"},
              "age": {"type": "integer"},
              "companies": {
                  "type": "array",
                  "items": {"type": "string"}
              },
              "net_worth": {"type": "string"}
          },
          "required": ["name", "age", "companies", "net_worth"],
          "additionalProperties": False
      }

      structured_llm = self.llm.with_structured_output(user_schema,method="json_schema",strict=True)

      response = structured_llm.invoke('Elon Reeve Musk (/ˈiːlɒn/ ⓘ EE-lon; born June 28, 1971) is a businessman and former public official who is the CEO and largest shareholder of Tesla and SpaceX. Musk has been the wealthiest person in the world since 2025, and briefly became the only trillionaire (in terms of US dollars) in June 2026; as of August 14, 2026, Forbes estimates his net worth to be US$864 billion.')

      user = User.model_validate(response)
      print(user.model_dump())



def main():

   agent = Agent()
   agent.Chat()


if __name__ == '__main__':
    main()