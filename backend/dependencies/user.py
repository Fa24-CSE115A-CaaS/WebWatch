from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlmodel import Session, select
from jose import JWTError, jwt
from auth_token import decode_access_token
# Dependencies
# from dependencies.task import get_task

# Schemas
from database import Database
# from schemas.task import Task
from schemas.user import User
import os

db = Database(os.getenv("ENV"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")
DbSession = Annotated[Session, Depends(db.get_session)]
token: str = Depends(oauth2_scheme)

async def get_user(session: DbSession, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        print(f"{payload} token \n\n")
        token_uuid: str = payload.get("id")
        if not token_uuid:
            raise credentials_exception
        
        user = session.exec(select(User).where(User.token_uuid == token_uuid)).first()
        if user is None:
            raise credentials_exception

        return user.id

    except JWTError:
        raise credentials_exception
