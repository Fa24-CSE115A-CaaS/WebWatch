import asyncio
from routers.user import router as user_router
from routers.task import router as task_router
from schemas.task import Task
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Database
from sqlmodel import select
from scheduler import Scheduler
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
scheduler = Scheduler()


# Setup database and CORS middleware based on environment
if os.getenv("ENV") == "PRODUCTION":
    origins = ["https://webwatch.live"]
else:
    origins = ["http://localhost:5173"]

db = Database(mode=os.getenv("ENV"))


# Lifespan event to start and stop tasks
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ON BOOT
    # START ALL ENABLED TASKS
    session = next(db.get_session())
    enabled_tasks = session.exec(select(Task).where(Task.enabled == True))
    reinit = [scheduler.add_task(task) for task in enabled_tasks]
    await asyncio.gather(*reinit)
    yield
    # ON SHUTDOWN
    await scheduler.shutdown()


# Initialize FastAPI with lifespan
app = FastAPI(root_path="/api", lifespan=lifespan)

# CORS Middleware (required for frontend to make requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # TODO: Change this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Defining existing endpoints
app.include_router(user_router)
app.include_router(task_router)


# NECESSARY FOR SWAGGER DOCS AUTHENTICATION SCHEMA
# Otherwise, the "Authorize" button uses /token instead of /api/users/token to authenticate...
# TODO: Find a better way to do this
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="WebWatchAPI",
        version="1.0.0",
        routes=app.routes,
    )
    # Set the OAuth2 security schema with the correct token URL
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {"password": {"tokenUrl": "/api/users/login", "scopes": {}}},
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
