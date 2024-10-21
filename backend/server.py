from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from schemas.task import Task, TaskCreate, TaskGet, TaskUpdate
from database import Database
from sqlmodel import select
from backend.utils.diff import diffFiles
from utils.notifications import send_mail
from utils.diff import get_latest_file, diffFiles

load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    # The root API, not much functionality
    return {"WebWatchAPI": "WebWatchAPI"}


@app.get("/tasks/status")
async def tasks_status(session_token: str, task_id: str | None = None):
    # Returns the status of task(s)
    return {"Tasks": []}


@app.post("/tasks", response_model=TaskGet, status_code=201)
async def tasks_create(body: TaskCreate, session_token: str):
    # TODO: Relate User with task
    db = Database()
    validated_task = Task.model_validate(body)
    with db.get_session() as session:
        session.add(validated_task)
        session.commit()
        session.refresh(validated_task)
    return validated_task


@app.put("/tasks/{task_id}", response_model=TaskGet)
async def tasks_update(task_id: int, body: TaskUpdate, session_token: str):
    db = Database()
    with db.get_session() as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        update_data = body.model_dump(exclude_unset=True)
        task.sqlmodel_update(update_data)
        session.add(task)
        session.commit()
        session.refresh(task)
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


@app.post("/tasks/[placehold]")  
async def scrape_and_check(url: str, session_token: str):
    db = Database()
    oldFile = None  
    with db.get_session() as session:
        # Replace with actual logic to fetch the old content
        task = session.exec(select(Task).where(Task.url == url)).first()

    
    scrape(url) # TODO: SCRAPE
    newFile = get_latest_file('scraper/scrapes', url)
    if not newFile: 
        raise HTTPException(status_code=404, detail="No new file found.")

    if diffFiles(oldFile, newFile): 
        # If changes are detected, send an email notification
        try:
            recipient_email = "user@example.com"  # TOdo: GET email from db
            send_mail(
                subject="Website Content Updated",
                message=f"The website '{url}' has been updated.",
                recipients=[recipient_email]
            )
            return {"status": "Changes detected and email sent!"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
    else:
        return {"status": "No changes detected."}
