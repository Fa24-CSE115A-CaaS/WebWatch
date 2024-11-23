from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
from database import Database
from schemas.user import User
from sqlmodel import select, Session

import os


app = FastAPI()
load_dotenv()

db = Database(mode=os.getenv("ENV"))

ACCESS_KEY = os.getenv("ACCESS_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_EXPIRATION = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

DbSession = Annotated[Session, Depends(db.get_session)]


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRATION)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ACCESS_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, ACCESS_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
