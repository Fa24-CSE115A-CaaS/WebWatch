from fastapi import APIRouter, HTTPException, Response
from schemas.task import Task, TaskCreate, TaskUpdate, TaskGet
from sqlmodel import select
from typing import List
from database import Database
from schemas.user import User

### TASK ENDPOINTS ###

router = APIRouter(
    prefix="/tasks",
)

db = Database(production=False)


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
@router.put("/{task_id}", response_model=TaskGet)
async def tasks_update(task_id: int, task_update: TaskUpdate):
    with db.get_session() as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Update task fields
        update_data = task_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)

        session.add(task)
        session.commit()
        session.refresh(task)
    return task


# Delete task by id
@router.delete("/{task_id}", response_model=TaskGet)
async def tasks_delete(task_id: int):
    with db.get_session() as session:
        try:
            task = session.get(Task, task_id)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            
            # Log task before deletion

            session.delete(task)
            session.commit()
        
        
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error deleting task")
    
    return Response(status_code=204)

 