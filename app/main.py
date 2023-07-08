from fastapi import FastAPI,Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
from dotenv import load_dotenv
import os
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
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

@app.get('/')
def root():
    return {'message':'running'}

@app.get('/posts')
def get_posts(db : Session = Depends(get_db)):
    # cursor.execute('''Select * from posts''')
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {'data':posts}

@app.post('/posts',status_code=status.HTTP_201_CREATED)
def create_posts(post : Post,db : Session = Depends(get_db)):
    # cursor.execute('''insert into posts (title,content,published) values (%s,%s,%s) returning *''',(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'message':'post created',
            'post':new_post}

@app.get('/posts/{id}')
def get_post(id : int,db : Session = Depends(get_db)):
    # cursor.execute('''select * from posts where id = %s''',(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id : {id} was not found')
    return {"post_detail":post}

@app.delete('/posts/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db : Session = Depends(get_db)):
    # cursor.execute('''delete from posts where id = %s returning *''',(str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id : {id} does not exist')
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id : int, post:Post,db : Session = Depends(get_db)):
    # cursor.execute('''update posts set title=%s,content=%s,published=%s where id=%s returning *''',(post.title,post.content,post.published,str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_to_update_query = db.query(models.Post).filter(models.Post.id==id)
    if not post_to_update_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id : {id} does not exist')
    post_to_update_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return {'message':'post updated',
            'data':post_to_update_query.first()}