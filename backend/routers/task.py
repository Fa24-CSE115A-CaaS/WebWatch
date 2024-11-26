from fastapi import (
    APIRouter,
    WebSocket,
    HTTPException,
    status,
    Depends,
    WebSocketDisconnect,
)
from schemas.task import Task, TaskCreate, TaskUpdate, TaskGet
from sqlmodel import Session, select
from typing import Annotated, List
from database import Database
from schemas.user import User
from dependencies.task import get_task
from dependencies.user import get_user, get_user_id
from scheduler import Scheduler, get_scheduler
from task_websocket_manager import get_task_manager
import os
import logging

### TASK ENDPOINTS ###

router = APIRouter(
    prefix="/tasks",
)

db = Database(mode=os.getenv("ENV"))
manager = get_task_manager()

DbSession = Annotated[Session, Depends(db.get_session)]
SchedulerDep = Annotated[Scheduler, Depends(get_scheduler)]
UserData = Annotated[User, Depends(get_user)]
TaskData = Annotated[Task, Depends(get_task)]

logging.basicConfig(level=logging.INFO)


# Create a new task
@router.post("", response_model=TaskGet, status_code=status.HTTP_201_CREATED)
async def tasks_create(
    task_create: TaskCreate,
    session: DbSession,
    scheduler: SchedulerDep,
    user_id: UserData,
):
    """
    Create a new task for the currently authenticated user.
    """
    logging.info(f"Creating task for user {user_id}")

    task = Task(**task_create.model_dump(), user_id=user_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    await scheduler.add_task(task)
    manager.notify_conections(user_id)
    return task


# List all tasks
@router.get("", response_model=List[TaskGet])
async def tasks_list(session: DbSession, user: UserData):
    """
    List all tasks for the currently authenticated user.
    """

    logging.info(f"Listing tasks for user {user.id}")
    tasks = session.exec(select(Task).where(Task.user_id == user)).all()
    return tasks


@router.websocket("/ws")
async def tasks_list_stream(token: str, websocket: WebSocket, session: DbSession):
    user_id = get_user_id(session, token)
    if user_id == None:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    ws_event = manager.connect(user_id)
    try:
        while True:
            tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
            serialized_tasks = ",".join([task.model_dump_json() for task in tasks])
            await websocket.send_text(f"[{serialized_tasks}]")
            await ws_event.wait()
            session.expire_all()
            ws_event.clear()
    except WebSocketDisconnect:
        manager.disconnect(user_id, ws_event)


@router.put("/{task_id}", response_model=TaskGet)
async def tasks_update(
    task_id: int,
    task_update: TaskUpdate,
    session: DbSession,
    user_id: UserData,
    scheduler: SchedulerDep,
):
    """
    Update a task by ID which belongs to the currently authenticated user.
    """
    logging.info(f"Updating task {task_id}")

    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    if task.user_id != user_id:
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
    manager.notify_conections(user_id)
    return task


# Delete task by id
@router.delete("/{task_id}", status_code=204)
async def tasks_delete(
    task_id: TaskData, session: DbSession, scheduler: SchedulerDep, user_id: UserData
):
    # Delete a task by ID which belongs to the currently authenticated user.
    task = session.get(Task, task_id)
    session.delete(task)
    session.commit()
    await scheduler.remove_task(task)
    manager.notify_conections(user_id)
