from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas,models, utils, oauth2, database
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags = ['Authentication']
)

@router.post('/login')
def login(user_cred : OAuth2PasswordRequestForm=Depends(),db : Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid credentials')
    if not utils.verify(user_cred.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid credentials')
    # create token
    access_token = oauth2.create_access_token(data={'user_id':user.id})
    return {'access_token':access_token,
            'token_type':'bearer'}