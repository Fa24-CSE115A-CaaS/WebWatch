from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr

class UserBase(SQLModel):
    email: str
    password_hash: str

class User(UserBase, table=True):
    id: int = Field(primary_key=True)

class UserGet(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str  

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

class UserOutput(BaseModel):
    email: EmailStr
    username: str
