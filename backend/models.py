from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):  # `table=True` to define it as a table
    id: int = Field(default=None, primary_key=True)  # Primary key field
    email: str = Field(max_length=50, unique=True)  # Unique constraint
    # token: str = Field(token=50, unique = True)
    password: str = Field(max_length=50)
