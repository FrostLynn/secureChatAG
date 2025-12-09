from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from pydantic import BaseModel
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from database import get_session
import crud, models
import os
from dotenv import load_dotenv

load_dotenv() # Load env vars before Config reads os.environ

# Secret key for JWT
SECRET_KEY = "dummy_secret_key_for_dev_only_change_me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# OAuth Configuration
# In production, use .env file
config = Config(environ=os.environ)
oauth = OAuth(config)

# You must set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in your shell/env
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None:
            return None
        return TokenData(username=username, user_id=user_id)
    except JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    token_data = await verify_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = crud.get_user_by_id(session, token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
