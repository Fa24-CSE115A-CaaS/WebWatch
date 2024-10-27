from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class UserBase(SQLModel):
    email: str
    password_hash: str

class User(UserBase, table=True):
    id: int = Field(primary_key=True)

class UserGet(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: str | None = None
    password_hash: str | None = None

    class Config:
        orm_mode = True

class UserDelete(BaseModel):
    pass
