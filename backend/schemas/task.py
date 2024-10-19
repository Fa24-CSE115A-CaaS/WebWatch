from sqlmodel import SQLModel, Field
from pydantic import field_validator
import json


NOTIFICATION_OPTIONS = {'EMAIL', 'DISCORD', 'SLACK'}

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    content: str | None
    url: str
    discord_url: str | None
    enabled_notification_options: str = "[]"
    
    @field_validator('enabled_notification_options')
    @classmethod
    def notification_choice_validator(cls, value: str):
        options = json.loads(value)
        unique = set()
        
        if not isinstance(options, list):
            raise ValueError(f'enabled_notification_options is not a valid json serialized list')
        
        for option in options:
            if option not in NOTIFICATION_OPTIONS:
                raise ValueError(f'enabled_notification_options contains invalid value')
            if option in unique:
                raise ValueError(f'duplicate notification option not allowed {option}')
            unique.add(option)
        return value
        
        