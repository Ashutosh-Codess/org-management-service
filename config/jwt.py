from datetime import datetime, timedelta
from jose import jwt, JWTError
import os

JWT_SECRET = os.getenv('JWT_SECRET', 'change-me-in-production')
JWT_ALGO = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGO)
    return token

def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload
    except JWTError:
        return None
