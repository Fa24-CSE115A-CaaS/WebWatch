from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
from database import Database
import secrets
import os
from schemas.user import User
from sqlmodel import SQLModel, select, Session
app = FastAPI()
load_dotenv()

db = Database(production=False)

ACCESS_KEY = os.getenv("ACCESS_SECRET_KEY")
REFRESH_KEY = os.getenv("REFRESH_SECRET_KEY")
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

'''
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=refresh_expiration)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_KEY, algorithm=ALGORITHM)
    return encoded_jwt
'''

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, ACCESS_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        uuid: str = payload.get("id")
        if not uuid:
            raise credentials_exception
        #token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    with db.get_session() as session:
        user = session.exec(select(User).where(User.token_uuid == uuid)).first()
        if user is None:
            raise credentials_exception
    return user