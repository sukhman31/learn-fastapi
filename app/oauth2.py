from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

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
    print('-----------------------------------------')
    print(expire)
    print('-----------------------------------------')
    to_encode.update({'expire':str(expire)})
    jwt_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return jwt_token