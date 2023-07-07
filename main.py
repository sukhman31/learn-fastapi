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

my_posts = [{'title':'title 1','content':'content 1','id':1},
            {'title':'title 2','content':'content 2','id':2}]

@app.get('/')
def root():
    return {'message':'running'}

@app.get('/posts')
def get_posts():
    return {"data":my_posts}

@app.post('/posts')
def create_post(new_post : Post):
    print(new_post.rating)
    print(new_post.dict())
    return new_post