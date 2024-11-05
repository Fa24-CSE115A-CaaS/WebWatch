from fastapi import APIRouter, HTTPException, status, Depends, Cookie
# from fastapi.responses import Response
from sqlmodel import SQLModel, select, Session
from schemas.user import UserRegister, UserLogin, UserOutput, User, TokenPair
from auth.password import get_hashed_password, verify_password
from auth.token import create_access_token, create_refresh_token, decode_access_token
from fastapi.security import OAuth2PasswordRequestForm

from database import Database
from datetime import timedelta
# from typing import Annotated

db = Database(production=False)

router = APIRouter(
    prefix="/user",
)

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED, 
    response_model=UserOutput,
    responses={
        status.HTTP_409_CONFLICT: {"description": "Email already registered"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)
async def create_user(user: UserRegister):
    with db.get_session() as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == user.email)).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        # Hash the password and create a new user
        hashed_password = get_hashed_password(user.password)
        new_user = User(email=user.email, password_hash=hashed_password)
        
        try:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

        return new_user

# Authenticates existing user
@router.post(
    '/login',
    status_code=status.HTTP_200_OK,
    response_model=TokenPair,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Incorrect email or password"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)
async def login(request: UserLogin):
    with db.get_session() as session:
        try:
            # Query the user based on email
            user = session.exec(select(User).where(User.email == request.email)).first()
            if not user or not verify_password(user.password_hash, request.password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect email or password"
                )

            # Generate tokens
            access_token = create_access_token(
                data={"id": user.token_uuid}, 
            )
            refresh_token = create_refresh_token(
                data={"id": user.token_uuid, "type": "refresh"},
            )

            return {"access_token": access_token, "refresh_token": refresh_token}
        except HTTPException as e:
            raise e

@router.get("/verify")
async def verify(token: str):
    payload = decode_access_token(token)
    uuid = payload.get("id")
    
    with db.get_session() as session:
        user = session.exec(select(User).where(User.token_uuid == uuid)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return {"email": user.email}

'''
# Get user details by ID
@router.get("/{user_id}")
async def get_user(user_email: int):
    with db.get_session() as session:
        user = session.exec(select(User).where(User.email == user_email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No User Found")
    return userOutput(email=user.email)


# Update user details by id
@router.put("/{user_id}")
async def users_update(user_id: int):
    with db.get_session() as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


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
'''