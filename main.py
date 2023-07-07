from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

@app.get('/')
def root():
    return {'message':'running'}

@app.post('/create_post')
def create_post(new_post : Post):
    print(new_post)
    return{"data":"new post"}