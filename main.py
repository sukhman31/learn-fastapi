from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{'title':'title 1','content':'content 1','id':1},
            {'title':'title 2','content':'content 2','id':2}]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

@app.get('/')
def root():
    return {'message':'running'}

@app.get('/posts')
def get_posts():
    return {"data":my_posts}

@app.post('/posts')
def create_posts(new_post : Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0,100000000)
    my_posts.append(post_dict)
    return {'message':'post created',
            'post':post_dict}

@app.get('/posts/{id}')
def get_post(id : int):
    post = find_post(id)
    return {"post_detail":post}