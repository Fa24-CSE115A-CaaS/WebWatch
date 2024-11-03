from sqlmodel import SQLModel, Field
from pydantic import BaseModel, validator, EmailStr
from datetime import datetime



class UserBase(SQLModel):
    email: str
    password_hash: str

class User(UserBase, table=True):
    id: int = Field(primary_key=True)

class UserGet(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

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

class UserOutput(BaseModel):
    email: EmailStr
    username: str

class UserRegister(BaseModel):
    email:EmailStr
    username: str
    password: str

""" class UserRegister(BaseModel):
    password: str
    confirm_password: str

    @validator("confirm_password")
    def verify_password_match(cls, v, values, **kwargs):
        password = values.get("password")
        if v != password:
            raise ValueError("The two passwords did not match.")
        return v """

class JwtTokenSchema(BaseModel):
    token: str
    payload: dict
    expire: datetime

class TokenPair(BaseModel):
    access: JwtTokenSchema
    refresh: JwtTokenSchema

class RefreshToken(BaseModel):
    refresh: str
