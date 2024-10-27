## Package Multipart used for decoding Json data
## python-jose - Used to do some password hashing 
# and as well related to our jwt tokensed used for authications
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext  # Fix typo here
from sqlalchemy import Column, Integer, String, Boolean
from dotenv import load_dotenv
from schemas.User import userInDB
from utils.hashing import get_hashed_password, verify_password
import os

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 1440  # 1 day

ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")  # Retrieve SECRET_KEY from the environment
ALGORITHM = "HS256"


""" Encrypt plaintext(password) with 
    Owner "Arms are weak, Moms spagetthi = dsfndslafgngnewognosng"

    Hash user's input to check if it matches with correct password
    User input = dsfndslafgngnewognosng

    Owner password == User's input; Authorize User
    
"""

def get_user(db, email: str):
    if email in db:
        user_data = db[email]
        return UserInDB(**user_data)



def authenticate_user(db, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    
    return user

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()  # Ensure we are copying the data to a new dictionary
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    # Create the token using the secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_CONTINUE, detail="Could not validate credentials", headers={"WWW-Authenticate" : "Bearer"})

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # get user stored in token
        if username is None:
            raise credential_exception
    except JWTError:
        raise credential_exception

    user = get_user(db, username=token_data.username) # dummy data
    if user is None:
        raise credential_exception
    
    return user

async def get_current_active_user(current_user: userInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


