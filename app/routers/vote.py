from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from .. import models,schemas,database,oauth2
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(
    prefix='/vote',
    tags=['VOTE']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db : Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id==vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'User with id {current_user.id} has already voted on post with id {vote.post_id}')
        new_vote = models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message':'successfully voted'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Vote does not exist')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message':'successfully removed vote'}