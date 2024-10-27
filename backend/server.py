from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from dotenv import load_dotenv
from schemas.task import Task, TaskCreate, TaskGet, TaskUpdate
from schemas.User import userCreate, userOutput, userRequest
from schemas.token import Token
from sqlmodel import select, Session
import asyncio
from database import Database
from scheduler import Scheduler
from utils.hashing import get_hashed_password, verify_password
import models
import os
from starlette.status import HTTP_404_NOT_FOUND
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from auth import create_access_token, authenticate_user, verify_password, create_refresh_token
from starlette import status
import logging

load_dotenv()
scheduler = Scheduler()
db = Database(production=True)

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


@app.put("/tasks/status", response_model=TaskGet)
async def tasks_update(task_id: int, session_token: str | None = None):
    with db.get_session() as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks/create", response_model=TaskGet, status_code=201)
async def tasks_create(body: TaskCreate, session_token: str | None = None):
    # TODO: Relate User with task
    validated_task = Task.model_validate(body)
    with db.get_session() as session:
        session.add(validated_task)
        session.commit()
        session.refresh(validated_task)
    return validated_task


@app.put("/tasks/update", response_model=TaskGet)
async def tasks_update(
    task_id: int, body: TaskUpdate, session_token: str | None = None
):
    with db.get_session() as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        update_data = body.model_dump(exclude_unset=True)
        task.sqlmodel_update(update_data)
        session.add(task)
        session.commit()
        session.refresh(task)

    # Start task if enabled
    if task.enabled:
        await scheduler.add_task(task)
    else:
        await scheduler.remove_task(task)
    return task


@app.put("/tasks/remove", response_model=TaskGet)
async def tasks_remove(task_id: int, session_token: str | None = None):
    with db.get_session() as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(task)
        session.commit()

    await scheduler.remove_task(task)

    return task


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
