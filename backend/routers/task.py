from fastapi import APIRouter, Depends, HTTPException, status, Path
from schemas.task import Task, TaskCreate, TaskUpdate, TaskGet
from sqlmodel import Session, select
from typing import Annotated, List
from database import Database
from schemas.user import User
from auth_token import get_current_user
from dependencies.task import get_task
from scheduler import Scheduler, get_scheduler
import os
import logging

### TASK ENDPOINTS ###

router = APIRouter(
    prefix="/tasks",
)

db = Database(mode=os.getenv("ENV"))

DbSession = Annotated[Session, Depends(db.get_session)]
SchedulerDep = Annotated[Scheduler, Depends(get_scheduler)]
UserData = Annotated[User, Depends(get_current_user)]
TaskData = Annotated[Task, Depends(get_task)]

logging.basicConfig(level=logging.INFO)

# Create a new task
@router.post("", response_model=TaskGet, status_code=status.HTTP_201_CREATED)
async def tasks_create(
    task_create: TaskCreate, session: DbSession, scheduler: SchedulerDep, user: UserData
):
    """
    Create a new task for the currently authenticated user.
    """
    logging.info(f"Creating task for user {user.id}")

    task = Task(**task_create.model_dump(), user_id=user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    await scheduler.add_task(task)
    return task


# List all tasks
@router.get("", response_model=List[TaskGet])
async def tasks_list(session: DbSession, user: UserData):
    """
    List all tasks for the currently authenticated user.
    """

    logging.info(f"Listing tasks for user {user.id}")
    tasks = session.exec(select(Task).where(Task.user_id == user.id)).all()
    return tasks


# Update task details by id
@router.put("/{task_id}", response_model=TaskGet)
async def tasks_update(
    task_id: TaskData,
    task_update: TaskUpdate,
    session: DbSession,
    scheduler: SchedulerDep,
):
    """
    Update a task by ID which belongs to the currently authenticated user.
    """
    logging.info(f"Updating task {task_id}")

    task = session.get(Task, task_id)
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
    """
    Delete a task by ID which belongs to the currently authenticated user.
    """

    task = session.get(Task, task_id)
    session.delete(task)
    session.commit()
    await scheduler.remove_task(task)
