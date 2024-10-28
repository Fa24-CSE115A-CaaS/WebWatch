from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Response, Depends
from dotenv import load_dotenv
from sqlmodel import SQLModel, select, Session
import asyncio
from typing import List
from schemas.task import Task, TaskCreate, TaskGet, TaskUpdate
from schemas.user import User, UserCreate, UserGet, UserUpdate, userOutput
from schemas.token import Token
from database import Database
from scheduler import Scheduler
from utils.hashing import get_hashed_password, verify_password
from starlette.status import HTTP_404_NOT_FOUND
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from auth import create_access_token, authenticate_user, verify_password, create_refresh_token
from starlette import status
import models
import os
import asyncio

scheduler = Scheduler()

db = Database(production=True)

load_dotenv()

# Dependency
def get_db() -> Session:
    with db.get_session() as session:
        yield session


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

# Create a new user
@app.post("/users", response_model=UserGet, status_code=201)
async def users_create(user_create: UserCreate):
    with db.get_session() as session:
        user = User(email=user_create.email, password_hash=user_create.password_hash)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

# List all users
# @app.get("/users", response_model=List[UserGet])
# async def users_list():
#     with db.get_session() as session:
#         users = session.exec(select(User)).all()
#     if not users:
#         raise HTTPException(status_code=404, detail="No users found")
#     return users

# Get a user by id
@app.get("/users/{user_id}", response_model=UserGet)
async def users_get(user_id: int):
    with db.get_session() as session:
        user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
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
    with db.get_session() as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete all tasks associated with the user
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        for task in tasks:
            session.delete(task)

        session.delete(user)
        session.commit()
    return Response(status_code=204)

# Task Endpoints

# Create a new task
@app.post("/tasks", response_model=TaskGet, status_code=201)
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
@app.get("/tasks", response_model=List[TaskGet])
async def tasks_list():
    with db.get_session() as session:
        tasks = session.exec(select(Task)).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks

# Update task details by id
@app.put("/tasks/{task_id}", response_model=TaskGet)
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
@app.delete("/tasks/{task_id}", response_model=TaskGet)
async def tasks_delete(task_id: int):
    # Delete a task
    with db.get_session() as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(task)
        session.commit()

    await scheduler.remove_task(task)
    return Response(status_code=204)

@app.get("/user/authentication")
async def user_authentication(hash: str):
    # For the authentication of existing accounts
    return {"Session Token": "PLACEHOLDER", "Status": 0}

@app.post("/user/register", response_model=userOutput, status_code=201)
def create_user(user: userCreate, db: Session = Depends(get_db)):
    
    # Create a new User instance
    hashed_password = get_hashed_password(user.password)
    new_user = models.User(username=user.username, email=user.email, password=hashed_password)
    logger.info(f"create password: {hashed_password}, verifying password.")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return userOutput(email=new_user.email)

@app.post('/user/login')
def login(request: userRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if user is None:
        logger.warning(f"Login failed: No user found with email {request.email}.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    
    # Verify the hashed password against the stored hash
    hashed_password = get_hashed_password(request.password) 
    if not verify_password(request.password, hashed_password):
        logger.warning(f"Login failed for email {request.email}: Incorrect password.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    token = create_access_token(data={"sub": user.email, "user_id": user.id})  # Include user ID in the token payload
    access_token = create_access_token(data = {'email': user.email})
    return {"access_token" : access_token, "token_type": "bearer", "email": user.email }

@app.get("/users/{user_id}", response_model= userOutput)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()  # Corrected the query syntax
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No User Found")
    return user



@app.get("/user/update")
async def user_update(hash: str, contents: str | None = None):
    # For changing passwords, updating emails, deleting accounts, etc.
    return {"Session Token": "PLACEHOLDER", "Status": 0}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
