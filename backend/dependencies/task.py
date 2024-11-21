from fastapi import HTTPException, Path, Depends
from typing import Annotated
from sqlmodel import Session

# Dependencies
from dependencies.user import get_user

# Schemas
from database import Database
from schemas.task import Task
from schemas.user import User
import os

db = Database(os.getenv("ENV"))

DbSession = Annotated[Session, Depends(db.get_session)]
UserData = Annotated[User, Depends(get_user)]


async def get_task(user: UserData, session: DbSession, task_id: int = Path()):
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="No task found with the given id")

    if task.user_id != user.id:
        raise HTTPException(
            status_code=403, detail="You do not have permission to access this task"
        )

    return task.id
