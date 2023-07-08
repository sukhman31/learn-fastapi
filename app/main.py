from fastapi import FastAPI
# from fastapi.params import Body
# from typing import Optional
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor 
# import time
# from dotenv import load_dotenv
# import os
from . import models
from .database import engine
from .routers import post,user

models.Base.metadata.create_all(bind=engine)
# load_dotenv('.env')

app = FastAPI()

# while True:
#     try:
#         conn = psycopg2.connect(host=os.getenv('DB_HOST'),database=os.getenv('DB_NAME'),user=os.getenv('DB_USERNAME'),password=os.getenv('DB_PASSWORD'),cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful')
#         break
#     except Exception as error:
#         print('Connection to database failed')
#         print(error)
#         time.sleep(3)

app.include_router(post.router)
app.include_router(user.router)

@app.get('/')
def root():
    return {'message':'running'}
