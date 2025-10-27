from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='db_fastapi', user='username', 
                                password='Passw0rd', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database coonection was successfulll.")
        break
    except Exception as e:
        print("DB connection error: ", e)
        time.sleep(5)


old_posts = [
    {"title": "post #1 title", "content": "post #1 content", "id": 1},
    {"title": "post #2 title", "content": "post #2 content", "id": 2}
    ]

@app.get('/')
def root():
    return {'message': 'fastapi'}

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}

@app.get('/posts')
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED) # change default status in decorator
def createposts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    post = cursor.fetchone()
    conn.commit()
    return {'new_post': post}

@app.get('/posts/{id}')
def get_post(id: int): # add ": int" for validation, id must be integer and will be converted in integer
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not found")
    print(post)
    return {"data": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    post = cursor.fetchone()
    conn.commit() 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, new_post: Post):
    
    cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING * """,
                   (new_post.title, new_post.content, new_post.published, str(id)))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not found")
    
    return {"data": post}