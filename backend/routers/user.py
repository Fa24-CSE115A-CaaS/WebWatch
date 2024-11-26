# Third-party imports
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlmodel import select, Session

# Local module imports
from schemas.user import (
    UserRegister,
    UserUpdate,
    UserOutput,
    User,
    Token,
    PasswordReset,
    PasswordResetRequest,
    DeleteAccountRequest,
)
from schemas.task import Task
from auth_password import get_hashed_password, verify_password
from auth_token import (
    create_access_token,
    decode_access_token,
)
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from utils.notifications import send_password_reset_email
from database import Database
from dependencies.user import get_user
from routers.task import tasks_delete

from database import Database
import logging
from scheduler import Scheduler, get_scheduler
from routers.task import tasks_delete
import os
import logging

### USER ENDPOINTS ###

db = Database(mode=os.getenv("ENV"))

router = APIRouter(
    prefix="/users",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")
DbSession = Annotated[Session, Depends(db.get_session)]
UserData = Annotated[User, Depends(get_user)]
SchedulerDep = Annotated[Scheduler, Depends(get_scheduler)]

# Configure logging
logging.basicConfig(level=logging.INFO)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=Token,
    responses={
        status.HTTP_409_CONFLICT: {"description": "Email already registered"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def create_user(user: UserRegister, session: DbSession):
    """
    Register a new user by providing an email and password.
    """

    logging.info(f"Registering user with email {user.email}")
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        logging.warning(f"Email {user.email} already registered")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    hashed_password = get_hashed_password(user.password)
    new_user = User(email=user.email, password_hash=hashed_password)

    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    user = session.exec(select(User).where(User.email == user.email)).first()
    access_token = create_access_token(
        data={"id": user.token_uuid},
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Incorrect email or password"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def login(session: DbSession, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Log in an already registered user by providing an email and password.
    """
    logging.info(f"User login attempt with email {form_data.username}")
    # Query the user based on email
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user:
        logging.warning(f"Incorrect email or password for {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    try:
        verify_password(user.password_hash, form_data.password)
    except ValueError:
        logging.warning(f"Incorrect email or password for {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    # Generate tokens
    access_token = create_access_token(
        data={"id": user.token_uuid},
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify")
async def verify(token: str, session: DbSession):
    """
    Verify a user's token.
    """

    logging.info(f"Verifying token")
    payload = decode_access_token(token)
    uuid = payload.get("id")

    user = session.exec(select(User).where(User.token_uuid == uuid)).first()
    if not user:
        logging.warning(f"User not found for token {token}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return {"email": user.email}


@router.get("/me", response_model=UserOutput)
async def read_users_me(current_user_id: UserData, session: DbSession):
    # Get the currently authenticated user's details using their access token.
    logging.info(f"Fetching current user {current_user_id}")
    user = session.exec(select(User).where(User.id == current_user_id)).first()
    return user


# Sends an email with a login link for password reset
@router.post("/email_auth", status_code=status.HTTP_200_OK)
async def email_auth(user_email: PasswordReset, session: DbSession):
    try:
        user = session.exec(select(User).where(User.email == user_email.email)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        reset_token = create_access_token(data={"id": user.token_uuid})
        reset_link = f"{os.getenv("FRONTEND_URL")}/auth/email_auth?token={reset_token}"
        send_password_reset_email(user_email.email, reset_link)
        return {"detail": "Email login link sent successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while sending the password reset email",
        )


# Resets the user's password after validating the request.
@router.post("/reset_password", status_code=status.HTTP_200_OK)
async def reset_password(
    reset_request: PasswordResetRequest,
    session: DbSession,
    current_user_id: UserData,
):
    try:
        user = session.get(User, current_user_id)
        user.password_hash = get_hashed_password(reset_request.new_password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"detail": "Password reset successful"}
    except Exception as e:
        logging.error(e)
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@router.delete("/delete")
async def delete_user(
    session: DbSession, current_user: UserData, scheduler: SchedulerDep
):
    user = session.get(User, current_user)

    # Query and delete all tasks associated with the user
    tasks = session.exec(select(Task).where(Task.user_id == user.id)).all()
    for task in tasks:
        await tasks_delete(task.id, session, scheduler)

    try:
        session.delete(user)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user",
        )
    return {"detail": "User and associated tasks deleted successfully"}


""" @router.put(
    "/{user_id}",
    response_model=UserOutput,
)
async def users_update(
    user_update: UserUpdate,
    session: DbSession,
    current_user: User = Depends(get_current_user),
    user_id: int = Path(..., description="The ID of the user to update"),
):
    # Update a user's account global variables, including Discord and Slack webhooks.
    logging.info(f"Updating user {user_id}")
    # Ensure the user is updating their own information
    if user_id != current_user.id:
        logging.warning(
            f"User {current_user.id} not authorized to update user {user_id}"
        )
        raise HTTPException(
            status_code=403, detail="Not authorized to update this user"
        )

    # Query the user again within the same session
    user = session.get(User, user_id)
    if not user:
        logging.warning(f"User {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")

    # Update fields that are provided in the request
    update_data = user_update.model_dump(
        exclude_unset=True
    )  # Exclude fields that weren't provided
    for key, value in update_data.items():
        setattr(user, key, value)
    try:
        session.add(user)
        session.commit()
        session.refresh(user)
    except Exception as e:
        logging.error(f"Error updating user {user_id}: {e}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    return user
 """
