from random import randrange
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

posts = [
    {"title": "post #1 title", "content": "post #1 content", "id": 1},
    {"title": "post #2 title", "content": "post #2 content", "id": 2}
    ]

@app.get('/')
def root():
    return {'message': 'fastapi'}

@app.get('/posts')
def get_posts():
    return {"data": posts}

@app.post('/posts')
def createposts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 100000000000)
    posts.append(post_dict)
    return {'new_post': post_dict}