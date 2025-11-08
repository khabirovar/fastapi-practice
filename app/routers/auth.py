from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    tags   = ["Auth"]
)

@router.post("/login", response_model=schemas.Token)
def login(creds: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == creds.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not utils.verify(creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    # create token
    # return token
    access_token = oauth2.create_access_token(data={"user_id": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}
