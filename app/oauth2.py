from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

load_dotenv('.env')

# SECRET_KEY
# ALGORITHM
# EXPIRATION TIME

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'expire':str(expire)})
    jwt_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return jwt_token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f'Could not validate credentials',
                                          headers={"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user