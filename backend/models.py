from typing import Optional
from sqlmodel import SQLModel, Field

class User(SQLModel,):  # 'table=True' marks this as a table model
    __tablename__ = "users"  # Define the table name
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    password: str = Field(index=True)
