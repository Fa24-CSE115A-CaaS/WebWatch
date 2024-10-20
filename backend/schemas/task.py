from sqlalchemy import Column
from typing import List, Literal
from sqlalchemy.types import JSON
from pydantic import field_validator
from sqlmodel import SQLModel, Field


NotificationOptions = List[Literal['EMAIL', 'DISCORD', 'SLACK']]

class TaskBase(SQLModel):
    name: str = Field(max_length=50)
    content: str | None = None
    url: str
    discord_url: str | None = None
    enabled_notification_options: NotificationOptions = Field(default=['EMAIL'], sa_column=Column(JSON()))
    
    @field_validator('enabled_notification_options')
    @classmethod
    def notification_choice_validator(cls, value: NotificationOptions):
        unique = set()
        for option in value:
            if option in unique:
                raise ValueError(f'duplicate notification option not allowed {option}')
            unique.add(option)
        return value
    
class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
class TaskGet(TaskBase):
    id: int
    
class TaskCreate(TaskBase):
    pass
    
class TaskUpdate(TaskBase):
    name: str | None = Field(default=None, max_length=50)
    url: str | None = None
    enabled_notification_options: NotificationOptions | None = Field(default=None, sa_column=Column(JSON()))
        