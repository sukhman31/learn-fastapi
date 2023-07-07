from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get('/')
def root():
    return {'message':'running'}

@app.post('/create_post')
def create_post(payload : dict = Body(...)):
    print(payload)
    return{"new_post":f'created new post with title:{payload["title"]} and content:{payload["content"]}'}