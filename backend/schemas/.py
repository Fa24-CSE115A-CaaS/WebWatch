from pydantic import BaseModel, EmailStr
from typing import Optional

class userCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class userRequest(BaseModel):
    email: EmailStr
    password: str

class userOutput(BaseModel):
    email: EmailStr

class userInDB(BaseModel):
    email: EmailStr
    hashed_password: str
    disabled: bool = False
