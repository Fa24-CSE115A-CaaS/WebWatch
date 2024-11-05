from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from argon2 import PasswordHasher
from dotenv import load_dotenv
import secrets
import os

app = FastAPI()
load_dotenv()

ACCESS_KEY = os.getenv("ACCESS_SECRET_KEY")
REFRESH_KEY = secrets.token_urlsafe(32)  # Generates a secure, 32-character key
ALGORITHM = os.getenv("ALGORITHM", "HS256")
access_expiration = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
refresh_expiration = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=access_expiration)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ACCESS_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=refresh_expiration)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_hashed_password(plain_password: str) -> str:
    return PasswordHasher().hash(plain_password)

def verify_password(hashed_password: str, plain_password: str) -> bool:
    return PasswordHasher().verify(hashed_password, plain_password)