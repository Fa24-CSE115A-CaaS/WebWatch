## Package Multipart used for decoding Json data
## python-jose - Used to do some password hashing 
# and as well related to our jwt tokensed used for authications
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext  # Fix typo here


SECRET_KEY = "53f9fe80552077e040867678575ac9129e2adc538e38c4a858eb457833b848e8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None 

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], depreact="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

""" Encrypt plaintext(password) with 
    Owner "Arms are weak, Moms spagetthi = dsfndslafgngnewognosng"

    Hash user's input to check if it matches with correct password
    User input = dsfndslafgngnewognosng

    Owner password == User's input; Authorize User
    
"""

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire =  datetime.utcnow() = timedelta(minutes=15)

    to_encode.update({"exp":expire})
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

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    
    return current_user

@app.post("/token", reponse_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password) # dummy db
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate" : "Bearer"}) )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token {
        data=("sub" : user.username
        )
    }
