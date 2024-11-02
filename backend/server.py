import asyncio
from routers.user import router as user_router
from routers.task import router as task_router
from schemas.task import Task
from fastapi import FastAPI, APIRouter
from database import Database
from sqlmodel import SQLModel, select, Session
from scheduler import Scheduler
from typing import List
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()
scheduler = Scheduler()
db = Database(production=False)

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

# Initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

# Defining existing endpoints
app.include_router(user_router)
app.include_router(task_router)


@app.get("/")
async def root():
    # The root API, not much functionality
    return {"WebWatchAPI": "WebWatchAPI"}
