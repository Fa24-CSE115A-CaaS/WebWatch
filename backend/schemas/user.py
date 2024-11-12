from sqlmodel import SQLModel, Field
from pydantic import BaseModel, validator, EmailStr
from datetime import datetime
from typing import Optional
from uuid import uuid4
import re
import os


class UserBase(SQLModel):
    email: EmailStr
    password_hash: str


class User(UserBase, table=True):
    __tablename__ = "user"
    id: Optional[int] = Field(default=None, primary_key=True)
    # Used in JWTs to avoid exposing user db primary keys
    token_uuid: str = Field(default_factory=lambda: str(uuid4()))
    discord_default_webhook: Optional[str] = None
    slack_default_webhook: Optional[str] = None

class UserRegister(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, value):
        if os.getenv("ENV") != "development":
            if len(value) < 8:
                raise ValueError("Password must be at least 8 characters long")
            if not re.search(r"[A-Z]", value):
                raise ValueError("Password must contain at least one uppercase letter")
            if not re.search(r"[a-z]", value):
                raise ValueError("Password must contain at least one lowercase letter")
            if not re.search(r"[0-9]", value):
                raise ValueError("Password must contain at least one digit")
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
                raise ValueError("Password must contain at least one special character")
        return value

class UserLogin(BaseModel):
    email: EmailStr
    password: str

"""
class UserGet(UserBase):
    id: int

    class Config:
        orm_mode = True
"""

"""
class UserDelete(BaseModel):
    pass

class UserReset(BaseModel):
    email: EmailStr
    password: str
"""

class UserUpdate(BaseModel):
    discord_default_webhook: Optional[str] = None
    slack_default_webhook: Optional[str] = None


    class Config:
        orm_mode = True
        

class UserOutput(BaseModel):
    id: int
    email: EmailStr


class Token(BaseModel):
    access_token: str

class PasswordReset(BaseModel):
    email: EmailStr


class PasswordResetRequest(BaseModel):
    reset_token: str
    new_password: str
    confirm_password: str
