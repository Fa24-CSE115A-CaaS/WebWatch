from fastapi import APIRouter, HTTPException, status, Depends, Cookie
from sqlmodel import SQLModel, select, Session
from schemas.user import UserRegister, UserLogin, UserUpdate, UserOutput, User, Token
from auth_password import get_hashed_password, verify_password
from auth_token import (
    create_access_token,
    decode_access_token,
    get_current_user,
)  # , create_refresh_token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from database import Database
from datetime import timedelta

db = Database(production=False)

router = APIRouter(
    prefix="/users",
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=Token,
    responses={
        status.HTTP_409_CONFLICT: {"description": "Email already registered"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def create_user(user: UserRegister):
    with db.get_session() as session:
        # Check if user already exists
        existing_user = session.exec(
            select(User).where(User.email == user.email)
        ).first()
        if existing_user:
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


# Authenticates existing user
@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Incorrect email or password"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"},
    },
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with db.get_session() as session:
        # Query the user based on email
        user = session.exec(
            select(User).where(User.email == form_data.username)
        ).first()
        if not user or not verify_password(user.password_hash, form_data.password):
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
async def verify(token: str):
    payload = decode_access_token(token)
    uuid = payload.get("id")

    with db.get_session() as session:
        user = session.exec(select(User).where(User.token_uuid == uuid)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

    return {"email": user.email}


@router.get("/me", response_model=UserOutput)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/{user_id}", response_model=UserOutput)
async def users_update(user_id: int, user_update: UserUpdate):
    with db.get_session() as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update fields that are provided in the request
        update_data = user_update.dict(exclude_unset=True)  # Exclude fields that weren't provided
        for key, value in update_data.items():
            setattr(user, key, value)

        try:
            session.add(user)
            session.commit()
            session.refresh(user)
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail="Internal server error")
    return user

"""
# Delete a user by id
@router.delete("{user_id}")
async def users_delete(user_id: int):
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