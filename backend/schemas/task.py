from sqlmodel import SQLModel, Field
from pydantic import field_validator
from typing import Literal
import json


NotificationOptions = list[Literal['EMAIL', 'DISCORD', 'SLACK']]

class TaskBase(SQLModel):
    name: str = Field(max_length=50)
    content: str | None
    url: str
    discord_url: str | None
    
class TaskCreate(TaskBase):
    enabled_notification_options: NotificationOptions = []
    
    @field_validator('enabled_notification_options', mode='before')
    @classmethod
    def notification_choice_validator(cls, value: NotificationOptions):
        unique = set()
        for option in value:
            if option in unique:
                raise ValueError(f'duplicate notification option not allowed {option}')
            unique.add(option)
        return value
    
    # Transform to serialized json 
    @field_validator('enabled_notification_options', mode='after')
    @classmethod
    def serialize_list(cls, value: NotificationOptions):
        return json.dumps(value)

class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    enabled_notification_options: str = "[]"
        