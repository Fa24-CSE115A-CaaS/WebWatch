from fastapi import FastAPI
from dotenv import load_dotenv

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


@app.get("/tasks/create")
async def tasks_create(session_token: str):
    # For the initialization of new tasks
    # Should be followed with tasks_update
    return {"Task_Id": "PLACEHOLDER", "Status": 0}


@app.get("/tasks/update")
async def tasks_update(session_token: str, task_id: int, contents: str | None = None):
    # If contents is empty then delete the task
    # Parse contents with json for things like when to run, what to watch, etc.
    return {"Status": 0}


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
