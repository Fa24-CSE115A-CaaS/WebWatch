from sqlmodel import SQLModel, Field
from pydantic import BaseModel, validator, EmailStr
from datetime import datetime
from typing import Optional



class UserBase(SQLModel):
    email: str
    password_hash: str

class User(UserBase, table=True):
    __tablename__ = "user"  # Ensures SQLModel uses the correct table name
    id: Optional[int] = Field(default=None, primary_key=True)

'''
class UserGet(UserBase):
    id: int

    class Config:
        orm_mode = True
'''

class UserLogin(BaseModel):
    email: EmailStr
    password: str

'''
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password_hash: str | None = None

    class Config:
        orm_mode = True

class UserDelete(BaseModel):
    pass

class UserReset(BaseModel):
    email: EmailStr
    password: str
'''

class UserOutput(BaseModel):
    email: EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    @validator("confirm_password")
    def verify_password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError("The two passwords did not match.")
        return v

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
'''

class RefreshToken(BaseModel):
    refresh: str
'''