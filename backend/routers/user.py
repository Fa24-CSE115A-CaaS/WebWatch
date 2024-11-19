from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlmodel import select, Session
from schemas.user import UserRegister, UserUpdate, UserOutput, User, Token
from auth_password import get_hashed_password, verify_password
from auth_token import (
    create_access_token,
    decode_access_token,
    get_current_user,
)
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from database import Database
import os
import logging

db = Database(mode=os.getenv("ENV"))

router = APIRouter(
    prefix="/users",
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")

DbSession = Annotated[Session, Depends(db.get_session)]

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

    # Hash the password and create a new user
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

    # Generate token to sign in user
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
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get the currently authenticated user's details using their access token.
    """

    logging.info(f"Fetching current user {current_user.id}")
    return current_user


@router.put(
    "/{user_id}",
    response_model=UserOutput,
)
async def users_update(
    user_update: UserUpdate,
    session: DbSession,
    current_user: User = Depends(get_current_user),
    user_id: int = Path(..., description="The ID of the user to update"),
):
    """
    Update a user's account global variables, including Discord and Slack webhooks.
    """
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
# Delete a user by id
@router.delete("{user_id}")
async def users_delete(user_id: int = Path(..., description="The ID of the user to delete")):
"""
"""
    Delete a user by ID.
"""

"""
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
"""
