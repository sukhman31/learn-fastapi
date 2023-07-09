from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from .. import models,schemas,database,oauth2
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func
import json

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/',response_model=List[schemas.PostVoteResponse])
def get_posts(db : Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_user), limit: int = 10, skip:int = 0, search:Optional[str] = ''):
    # cursor.execute('''Select * from posts''')
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
    # print(posts)
    # posts = posts.all()
    posts = db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    response_data = []
    for post,votes in posts:
        response_data.append({
            'Post':post,
            'Votes':votes
        })  
    return response_data

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post : schemas.PostCreate,db : Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute('''insert into posts (title,content,published) values (%s,%s,%s) returning *''',(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id = current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}',response_model=schemas.PostVoteResponse)
def get_post(id : int,db : Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute('''select * from posts where id = %s''',(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id : {id} was not found')
    response_data = {
        'Post':post[0],
        'Votes':post[1]
    }
    return response_data

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db : Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute('''delete from posts where id = %s returning *''',(str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id==id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id : {id} does not exist')
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action')
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
    if post_to_update_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action')
    post_to_update_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return post_to_update_query.first()