from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone, timedelta
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

def decode_access_token(token: str) -> dict:
    try:
        # Decode the token
        payload = jwt.decode(token, ACCESS_KEY, algorithms=[ALGORITHM])
        
        # Check if the token has expired
        exp = payload.get("exp")
        if not exp or datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_hashed_password(plain_password: str) -> str:
    return PasswordHasher().hash(plain_password)

def verify_password(hashed_password: str, plain_password: str) -> bool:
    return PasswordHasher().verify(hashed_password, plain_password)