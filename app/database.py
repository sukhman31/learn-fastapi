from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv('.env')

username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
hostname = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')

SQLALCHEMY_DATABASE_URL = f'postgresql://{username}:{password}@{hostname}/{database}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

session_local = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()