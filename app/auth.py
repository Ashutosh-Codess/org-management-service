from passlib.context import CryptContext
from app.config import get_settings
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    password = password[:72]
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    password = password[:72]
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict, expires_delta: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    settings = get_settings()
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")

async def get_current_admin(token: str = Depends(oauth2_scheme)):
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        admin_email = payload.get("email")
        org_name = payload.get("org")

        if admin_email is None or org_name is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"email": admin_email, "organization": org_name}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

