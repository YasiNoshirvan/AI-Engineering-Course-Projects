
import dotenv
from typing import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import START, END, StateGraph

dotenv.load_dotenv()


class ContentState(TypedDict):
    topic: str
    draft: str
    score: int
    feedback: str
    revision_count: int


llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0.7)


def write_draft(state: ContentState):
    prompt = f'Write a short paragraph about: {state['topic']}'

    if state.get('feedback'):
        prompt += f'\n\nPrevious feedback to address: {state['feedback']}'

    response = llm.invoke(prompt)

    return {'draft': response.content, 'revision_count': state.get('revision_count', 0) + 1}


def review_draft(state: ContentState):
    prompt = f'''Rate this paragraph from 1-10 and give one sentence of feedback. be extremely strict.
    Paragraph: {state['draft']}
    
    Respond in exactly this format:
    Score: <number>
    Feedback: <text>'''

    response = llm.invoke(prompt)
    text = response.content

    score_line = [l for l in text.split('\n') if l.startswith('Score:')][0]
    feedback_line = [l for l in text.split(
        '\n') if l.startswith('Feedback:')][0]

    score = int(score_line.replace('Score:', '').strip())
    feedback = feedback_line.replace('Feedback:', '').strip()

    return {'score': score, 'feedback': feedback}


def should_revise(state: ContentState):
    if state['score'] >= 10:
        return END
    if state['revision_count'] >= 3:
        return END

    return 'write_draft'


builder = StateGraph(ContentState)

builder.add_node(write_draft)
builder.add_node(review_draft)

builder.add_edge(START, 'write_draft')
builder.add_edge('write_draft', 'review_draft')
builder.add_conditional_edges('review_draft', should_revise)

graph = builder.compile()

result = graph.invoke({
    'topic': 'why sleep matters for learning',
    'draft': '',
    'feedback': '',
    'score': 0,
    'revision_count': 0
})

print(f'Final draft ({result['revision_count']} revision(s)):\n')
print(result['draft'])
print(f'\nFinal Score: {result['score']}')



'''
from typing import TypedDict
from langgraph.graph import START,StateGraph  #start is another node


class Essay(TypedDict):
    topic:str
    content:str | None
    score:float | None


essay = Essay(topic = 'this is topic' , content ='this is content', score=5.5)


def write_essay(essay:Essay):
    return{'content':f'the essay is about {essay['topic']}'}

def score_essay(essay:Essay):
    return{'score':10}


builder=StateGraph(Essay)

builder.add_node(write_essay)
builder.add_node(score_essay)

builder.add_edge(START,'write_essay')
builder.add_edge('write_essay','score_essay')


graph = builder.compile()

state = graph.invoke({'topic':'programming', 'content':None, 'Score':None})

print(state)
'''

#######################################################################################################

'''
from langgraph.graph import StateGraph, END

def add(state:int):
    return state+1

def multiply(state:int):
    return state*2

def sould_continue(state):
    return END if state > 10 else 'multiply'

workflow = StateGraph(int)

workflow.add_node(add)
workflow.add_node(multiply)

workflow.add_edge('multiply','add')
workflow.add_conditional_edges('add', sould_continue)

workflow.set_entry_point('multiply')   #Start Point

app = workflow.compile()

print(app.invoke(1))
                '''
