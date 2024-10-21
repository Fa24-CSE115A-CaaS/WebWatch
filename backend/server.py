from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from schemas.task import Task, TaskCreate, TaskGet, TaskUpdate
from sqlmodel import select
import asyncio
from database import Database
from scheduler import Scheduler

load_dotenv()

scheduler = Scheduler()
db = Database()


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


@app.get("/user/authentication")
async def user_authentication(hash: str):
    # For the authentication of existing accounts
    return {"Session Token": "PLACEHOLDER", "Status": 0}


@app.get("/user/register")
async def user_register(email: str, hash: str):
    # For the creation of new accounts
    return {"Session Token": "PLACEHOLDER", "Status": 0}


@app.get("/user/update")
async def user_update(hash: str, contents: str | None = None):
    # For changing passwords, updating emails, deleting accounts, etc.
    return {"Session Token": "PLACEHOLDER", "Status": 0}
