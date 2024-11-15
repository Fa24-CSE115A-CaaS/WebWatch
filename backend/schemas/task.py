from sqlalchemy import Column
from typing import List, Literal
from sqlalchemy.types import JSON
from pydantic import field_validator
from sqlmodel import SQLModel, Field, Session, select
import asyncio
from schemas.user import User
import os


NotificationOptions = List[Literal["EMAIL", "DISCORD", "SLACK"]]

class TaskBase(SQLModel):
    name: str = Field(max_length=50)
    content: str | None = None
    url: str
    discord_url: str | None = None
    enabled_notification_options: NotificationOptions = Field(
        default=["EMAIL"], sa_column=Column(JSON())
    )
    enabled: bool = False  # If the task is enabled then it should be running

    @field_validator("enabled_notification_options")
    @classmethod
    def notification_choice_validator(cls, value: NotificationOptions):
        unique = set()
        for option in value:
            if option in unique:
                raise ValueError(f"duplicate notification option not allowed {option}")
            unique.add(option)
        return value

    def proc_init(self):
        # Initializes the async function in the new process
        return asyncio.run(self.run())

    async def run(self):
        # TODO: Implement scanning logic

        loop = asyncio.get_event_loop()
        user = await loop.run_in_executor(None, self.get_user)

        while self.enabled:
            await asyncio.sleep(1)
            print(f"User {user.email}: scan {self.name}")

            # Proof of concept for concurrently updating content in db after scanning
            # await loop.run_in_executor(None, self.update_content_in_db, "new content")


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")

    def get_id(self):
        # Returns the task_id
        return self.id

    def get_user(self):
        from database import Database
        db = Database(mode=os.getenv("ENV"))
        session = next(db.get_session())
        result = session.exec(select(User).where(User.id == self.user_id)).first()
        return result

    def update_content_in_db(self, new_content):
        from database import Database
        db = Database(mode=os.getenv("ENV"))
        session = next(db.get_session())
        task = session.exec(select(Task).where(Task.id == self.id)).first()
        if task:
            task.content = new_content
            session.add(task)
            session.commit()
        session.close()

class TaskGet(TaskBase):
    id: int
    user_id: int


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    name: str | None = Field(default=None, max_length=50)
    content: str | None = None
    url: str | None = None
    discord_url: str | None = None
    enabled_notification_options: NotificationOptions | None = Field(
        default=None, sa_column=Column(JSON())
    )
    enabled: bool | None = None
