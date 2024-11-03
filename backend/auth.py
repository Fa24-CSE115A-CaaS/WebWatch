from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from jose import JWTError, jwt
from argon2 import PasswordHasher
from dotenv import load_dotenv
import secrets
import os

app = FastAPI()
ph = PasswordHasher()

load_dotenv()
ACCESS_KEY = os.getenv("ACCESS_SECRET_KEY")
#REFRESH_KEY = os.getenv("REFRESH_SECRET_KEY")
REFRESH_KEY = secrets.token_urlsafe(32)  # Generates a secure, 32-character key

ALGORITHM = os.getenv("ALGORITHM", "HS256")
access_expiration = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
refresh_expiration = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Checks if User exist, if so verifies password
def authenticate_user(user):
    session.exec(select(User).where(User.email == request.email)).first()
    if not user:
        return False
    if not verify_password(user.hashed_password, password):
        return False
    return user

def create_access_token(data_data: dict, expires_delta: timedelta | None = None):
    payload = {}

    payload['user'] = user_data
    payload["exp"] = datetime.utcnow() + (
        expires_delta if expires_delta is not None else timedelta(minutes(ACCESS_TOKEN_EXPIRE_MINUTES)))
    token = jwt.encode(
        payload=payload, 
        key=ACCESS_SECRET_KEY,
        algorithm= ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=refresh_expiration)
    to_encode = {"exp": expires_delta, "sub": data.get("sub")}
    encoded_jwt = jwt.encode(to_encode, REFRESH_KEY, ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_CONTINUE, detail="Could not validate credentials", headers={"WWW-Authenticate" : "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # get user stored in token
        if username is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception
    
    return user

def get_hashed_password(plain_password):
    return ph.hash(plain_password)

def verify_password(hashed_password, plain_password):
    return ph.verify(hashed_password, plain_password)

def _get_utc_now():
    if sys.version_info >= (3, 2):
        # For Python 3.2 and later
        current_utc_time = datetime.now(timezone.utc)
    else:
        # For older versions of Python
        current_utc_time = datetime.utcnow()
    return current_utc_time

def get_user_by_email(email: str):
    with db.get_session() as session:
        user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user