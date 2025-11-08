from sqlalchemy.orm import Session
from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    
    prefix = "/posts",
    tags   = ["Posts"]
)

@router.get('', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # change default status in decorator
def createposts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.model_dump()) # unpack dict from pydantic model returning
    db.add(new_post)
    db.commit()          # sam as conn.commit()
    db.refresh(new_post) # same as RETURNING
    return new_post

@router.get('/{id}', response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)): # add ": int" for validation, id must be integer and will be converted in integer
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first() # same as WHERE; first() like all() execute generated sql query
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not found")
    print(post)
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # post = cursor.fetchone()
    # conn.commit() 
    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not found")
    
    post.delete()
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(id: int, new_post: schemas.PostCreate, db: Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING * """,
    #                (new_post.title, new_post.content, new_post.published, str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not found")
    
    post.update(new_post.model_dump())
    db.commit()

    return post.first()
