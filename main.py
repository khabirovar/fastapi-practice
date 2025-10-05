from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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

@app.get('/posts', status_code=status.HTTP_201_CREATED) # change default status in decorator
def get_posts():
    return {"data": posts}

@app.get('/posts/{id}')
def get_post(id: int, response: Response): # add ": int" for validation, id must be integer and will be converted in integer
    post = list(filter(lambda x: x['id'] == id, posts))
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"{id} does not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not found")
    print(post)
    return {"data": post}

@app.post('/posts')
def createposts(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 100000000000)
    posts.append(post_dict)
    return {'new_post': post_dict}