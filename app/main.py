from fastapi import FastAPI,Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from dotenv import load_dotenv
import os

load_dotenv('.env')

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host=os.getenv('DB_HOST'),database=os.getenv('DB_NAME'),user=os.getenv('DB_USERNAME'),password=os.getenv('DB_PASSWORD'),cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful')
        break
    except Exception as error:
        print('Connection to database failed')
        print(error)
        time.sleep(3)

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
    cursor.execute('''Select * from posts''')
    posts = cursor.fetchall()
    return {"data":posts}

@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):
    cursor.execute('''insert into posts (title,content,published) values (%s,%s,%s) returning *''',(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'message':'post created',
            'post':new_post}

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

@app.put('/posts/{id}')
def update_post(id : int, post:Post):
    index = find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id : {id} does not exist')
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {'data':post_dict}