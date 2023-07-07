from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get('/')
def root():
    return {'message':'running'}

@app.post('/create_post')
def create_post(new_post : Post):
    print(new_post.rating)
    print(new_post.dict())
    return new_post