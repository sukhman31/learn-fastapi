from fastapi import FastAPI,Response, status, HTTPException
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

def find_index_post(id):
    for i,post in enumerate(my_posts):
        if post['id'] == id:
            return i

@app.get('/')
def root():
    return {'message':'running'}

@app.get('/posts')
def get_posts():
    return {"data":my_posts}

@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(new_post : Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0,100000000)
    my_posts.append(post_dict)
    return {'message':'post created',
            'post':post_dict}

@app.get('/posts/{id}')
def get_post(id : int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id : {id} was not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f'post with id:{id} was not found'}
    return {"post_detail":post}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    index = find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id : {id} does not exist')
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)