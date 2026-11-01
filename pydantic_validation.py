from pydantic import BaseModel, Field

class User(BaseModel):
    #id:int
    #name:str = Field(min_length=2, max_length=50)
    name: str = Field(description = "The user's full name", examples = ['Alice' , 'Ali']) 
    #age:int

user = User(
    id ='1',
    name='Alice',
    age='25'
)

print(user)