from fastapi import APIRouter, HTTPException, status, Depends
from schemas.task import Task, TaskCreate, TaskUpdate, TaskGet
from sqlmodel import Session, select
from typing import Annotated, List
from database import Database
from schemas.user import User
from dependencies.task import get_task
from dependencies.user import get_user
from scheduler import Scheduler, get_scheduler
import os

### TASK ENDPOINTS ###

router = APIRouter(
    prefix="/tasks",
)

db = Database(mode=os.getenv("ENV"))

DbSession = Annotated[Session, Depends(db.get_session)]
SchedulerDep = Annotated[Scheduler, Depends(get_scheduler)]
UserData = Annotated[User, Depends(get_user)]
TaskData = Annotated[Task, Depends(get_task)]


# Create a new task
@router.post("", response_model=TaskGet, status_code=201)
async def tasks_create(task_create: TaskCreate, session: DbSession, scheduler: SchedulerDep, user: UserData):
    task = Task(**task_create.model_dump(), user_id=user)
    session.add(task)
    session.commit()
    session.refresh(task)
    await scheduler.add_task(task)
    return task


# List all tasks
@router.get("", response_model=List[TaskGet])
async def tasks_list(session: DbSession, user: UserData):
    tasks = session.exec(select(Task).where(Task.user_id == user)).all()
    return tasks


@router.put("/{task_id}", response_model=TaskGet)
async def tasks_update(
    task_id: int, task_update: TaskUpdate, session: DbSession, user: UserData, scheduler: SchedulerDep
):
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    if task.user_id != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task",
        )

    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    await scheduler.restart_task(task)
    return task


# Delete task by id
@router.delete("/{task_id}", status_code=204)
async def tasks_delete(task_id: TaskData, session: DbSession, scheduler: SchedulerDep):
    task = session.get(Task, task_id)
    session.delete(task)
    session.commit()
    await scheduler.remove_task(task)
