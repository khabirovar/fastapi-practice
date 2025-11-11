from jose import JWSError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

# SECRET_KEY
# Algorithm
# Expiration time

# openssl rand -hex 32
SECRET_KEY = "6edf6628c7b62aef8f22d05fc2f5706fed56b2aae0c78849c40c21f7dc50710c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = str(payload.get("user_id"))
        if not id:
            raise credential_exception
        token_data  = schemas.TokenData(id=id)
    except JWSError:
        raise credential_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", 
                                          headers={"WWW-authenticate": "Bearer"})
    
    token = verify_access_token(token, create_access_token)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user