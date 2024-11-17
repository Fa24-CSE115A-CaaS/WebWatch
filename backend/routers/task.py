from fastapi import APIRouter, Depends, HTTPException, status, Path
from schemas.task import Task, TaskCreate, TaskUpdate, TaskGet
from sqlmodel import Session, select
from typing import Annotated, List
from database import Database
from schemas.user import User
from auth_token import get_current_user
from dependencies.task import get_task
import os
import logging

### TASK ENDPOINTS ###

router = APIRouter(
    prefix="/tasks",
)

db = Database(mode=os.getenv("ENV"))

DbSession = Annotated[Session, Depends(db.get_session)]
UserData = Annotated[User, Depends(get_current_user)]
TaskData = Annotated[Task, Depends(get_task)]

logging.basicConfig(level=logging.INFO)

# Create a new task
@router.post("", response_model=TaskGet, status_code=status.HTTP_201_CREATED)
async def tasks_create(task_create: TaskCreate, session: DbSession, user: UserData):
    """
    Create a new task.

    Args:
        task_create (TaskCreate): The task creation details.
        session (DbSession): The database session.
        user (UserData): The current logged-in user.

    Returns:
        TaskGet: The newly created task.
    """
    logging.info(f"Creating task for user {user.id}")
    task = Task(**task_create.model_dump(), user_id=user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# List all tasks
@router.get("", response_model=List[TaskGet])
async def tasks_list(session: DbSession, user: UserData):
    """
    List all tasks for the current user.

    Args:
        session (DbSession): The database session.
        user (UserData): The current logged-in user.

    Returns:
        List[TaskGet]: A list of tasks for the current user.
    """
    logging.info(f"Listing tasks for user {user.id}")
    tasks = session.exec(select(Task).where(Task.user_id == user.id)).all()
    return tasks


# Update task details by id
@router.put("/{task_id}", response_model=TaskGet)
async def tasks_update(
    task_update: TaskUpdate,
    session: DbSession,
    task: TaskData,
    task_id: int = Path(..., description="The ID of the task to update"),
):
    """
    Update task details by ID.

    Args:
        task_id (int): The ID of the task to update.
        task_update (TaskUpdate): The updated task details.
        session (DbSession): The database session.
        task (TaskData): The task to update.

    Returns:
        TaskGet: The updated task.
    """
    logging.info(f"Updating task {task_id}")
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


# Delete task by id
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def tasks_delete(
    session: DbSession,
    task: TaskData,
    task_id: int = Path(..., description="The ID of the task to delete"),
):
    """
    Delete a task by ID.

    Args:
        task_id (int): The ID of the task to delete.
        session (DbSession): The database session.
        task (TaskData): The task to delete.

    Returns:
        None: A response with status code 204.
    """
    logging.info(f"Deleting task {task_id}")
    session.delete(task)
    session.commit()