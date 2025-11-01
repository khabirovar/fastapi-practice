from random import randrange
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user


models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)

@app.get('/')
def root():
    return {'message': 'fastapi'}
