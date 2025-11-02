from jose import JWSError, jwt
from datetime import datetime, timedelta

# SECRET_KEY
# Algorithm
# Expiration time

# openssl rand -hex 32
SECRET_KEY = "6edf6628c7b62aef8f22d05fc2f5706fed56b2aae0c78849c40c21f7dc50710c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt