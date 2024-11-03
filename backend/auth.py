from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from jose import JWTError, jwt
from argon2 import PasswordHasher
from dotenv import load_dotenv
import os

app = FastAPI()
ph = PasswordHasher()

load_dotenv()
ACCESS_KEY = os.getenv("ACCESS_SECRET_KEY")
REFRESH_KEY = os.getenv("REFRESH_SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM", "HS256")
access_expiration = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
refresh_expiration = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_hashed_password(plain_password):
    return ph.hash(plain_password)

def verify_password(hashed_password, plain_password):
    return ph.verify(hashed_password, plain_password)

def get_user(db, email: EmailStr):
    if email in db:
        user_data = db[email]
        return UserInDB(**user_data)

# Checks if User exist, if so verifies password
def authenticate_user(user):
    session.exec(select(User).where(User.email == request.email)).first()
    if not user:
        return False
    if not verify_password(user.hashed_password, password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=access_expiration)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ACCESS_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=refresh_expiration)

    to_encode = {"exp": expires_delta, "sub": data.get("sub")}
    encoded_jwt = jwt.encode(to_encode, REFRESH_KEY, ALGORITHM)
    return encoded_jwt

def decodeJWT(jwtoken: str):
    try:
        payload = jwt.decode(jwtoken,setting.secret_key, setting.algorithm)
        return payload
    except InvalidTokenError:
        return None

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decodeJWT(jwtoken)
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.JWTError:
            return False

def get_current_user(token: str = Depends(oauth2_scheme)):
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

