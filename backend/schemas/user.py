from sqlmodel import SQLModel, Field
from pydantic import BaseModel, validator, model_validator, EmailStr
from datetime import datetime
from typing import Optional
from uuid import uuid4
import re
import os


def validate_password(value: str) -> str:
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
    def password_validation(cls, value):
        return validate_password(value)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


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
    new_password: str
    confirm_password: str

    @model_validator(mode="after")
    def passwords_match(cls, values):
        new_password = values.new_password
        confirm_password = values.confirm_password
        if new_password != confirm_password:
            raise ValueError("Passwords do not match")
        validate_password(new_password)
        return values


class DeleteAccountRequest(BaseModel):
    password: str
