from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from sqlmodel import SQLModel, select
import asyncio
from typing import List
from schemas.task import Task, TaskCreate, TaskGet, TaskUpdate
from schemas.user import User, UserCreate, UserGet, UserUpdate  # Import schemas
from database import Database
from scheduler import Scheduler

load_dotenv()

scheduler = Scheduler()
db = Database(production=False)

SQLModel.metadata.create_all(db.engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ON BOOT
    # START ALL ENABLED TASKS
    with db.get_session() as session:
        enabled_tasks = session.exec(select(Task).where(Task.enabled == True))
        reinit = [scheduler.add_task(task) for task in enabled_tasks]
        await asyncio.gather(*reinit)
    yield
    # ON SHUTDOWN
    await scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    # The root API, not much functionality
    return {"WebWatchAPI": "WebWatchAPI"}

# User Endpoints

# List all users
@app.get("/users", response_model=List[UserGet])
async def users_list():
    with db.get_session() as session:
        users = session.exec(select(User)).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

# Get a user by id
@app.get("/users/{user_id}", response_model=UserGet)
async def users_get(user_id: int):
    with db.get_session() as session:
        user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Create a new user
@app.post("/users", response_model=UserGet, status_code=201)
async def users_create(user_create: UserCreate):
    with db.get_session() as session:
        user = User(email=user_create.email, password=user_create.password)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

# Update user details by id
@app.put("/users/{user_id}", response_model=UserGet)
async def users_update(user_id: int, user_update: UserUpdate):
    with db.get_session() as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

# Delete a user by id
@app.delete("/users/{user_id}", response_model=UserGet)
async def users_delete(user_id: int):
    # Delete a user
    with db.get_session() as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
    return user

# Task Endpoints

@app.post("/tasks/create", response_model=TaskGet, status_code=201)
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

@app.get("/tasks", response_model=List[TaskGet])
async def tasks_list():
    # List all tasks
    with db.get_session() as session:
        tasks = session.exec(select(Task)).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks

@app.put("/tasks/update/{task_id}", response_model=TaskGet)
async def tasks_update(task_id: int, task_update: TaskUpdate):
    # Update task details
    with db.get_session() as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        update_data = task_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
        session.add(task)
        session.commit()
        session.refresh(task)
    return task

@app.delete("/tasks/delete/{task_id}", response_model=TaskGet)
async def tasks_delete(task_id: int):
    # Delete a task
    with db.get_session() as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(task)
        session.commit()
    return task