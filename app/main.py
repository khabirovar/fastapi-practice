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

@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post('/posts', status_code=status.HTTP_201_CREATED) # change default status in decorator
def createposts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.model_dump()) # unpack dict from pydantic model returning
    db.add(new_post)
    db.commit()          # sam as conn.commit()
    db.refresh(new_post) # same as RETURNING
    return {'new_post': new_post}

@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)): # add ": int" for validation, id must be integer and will be converted in integer
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first() # same as WHERE; first() like all() execute generated sql query
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not found")
    print(post)
    return {"data": post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # post = cursor.fetchone()
    # conn.commit() 
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not found")
    
    post.delete()
    db.commit()
    
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