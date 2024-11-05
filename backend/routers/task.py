from fastapi import APIRouter, HTTPException
from schemas.task import Task, TaskCreate, TaskUpdate, TaskGet
from sqlmodel import select, Session
from typing import List
from database import Database
from schemas.user import User


### TASK ENDPOINTS ###

router = APIRouter(
    prefix="/task",
)

# Create a new task
@router.post("", response_model=TaskGet, status_code=201)
async def tasks_create(task_create: TaskCreate):
    # Validate user_id
    with db.get_session() as session:
        user = session.get(User, task_create.user_id)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid user_id")
        task = Task(**task_create.dict())
        session.add(task)
        session.commit()
        session.refresh(task)
    return task

# List all tasks
@router.get("", response_model=List[TaskGet])
async def tasks_list():
    with db.get_session() as session:
        tasks = session.exec(select(Task)).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks

# Update task details by id
@router.put("{task_id}", response_model=TaskGet)
async def tasks_update(task_id: int, task_update: TaskUpdate):
    with db.get_session() as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        update_data = task_update.dict(exclude_unset=True)
        # TODO: Find a better way to exclude user_id... const/static values in Model/Schema??
        # Exclude user_id from being updated
        if "user_id" in update_data:
            del update_data["user_id"]
        for key, value in update_data.items():
            setattr(task, key, value)
        session.add(task)
        session.commit()
        session.refresh(task)
    return task

# Delete task by id
@router.delete("{task_id}", response_model=TaskGet)
async def tasks_delete(task_id: int):
    # Delete a task
    with db.get_session() as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(task)
        session.commit()
    return Response(status_code=204)