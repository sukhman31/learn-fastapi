from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from .. import models,schemas,database,oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/')
def get_posts(db : Session = Depends(database.get_db),response_model=List[schemas.PostResponse],current_user = Depends(oauth2.get_current_user)):
    # cursor.execute('''Select * from posts''')
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post : schemas.PostCreate,db : Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute('''insert into posts (title,content,published) values (%s,%s,%s) returning *''',(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}',response_model=schemas.PostResponse)
def get_post(id : int,db : Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute('''select * from posts where id = %s''',(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id : {id} was not found')
    return post

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db : Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
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

@router.put('/{id}',response_model=schemas.PostResponse)
def update_post(id : int, post:schemas.PostCreate,db : Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute('''update posts set title=%s,content=%s,published=%s where id=%s returning *''',(post.title,post.content,post.published,str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_to_update_query = db.query(models.Post).filter(models.Post.id==id)
    if not post_to_update_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id : {id} does not exist')
    post_to_update_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return post_to_update_query.first()