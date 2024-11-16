from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import select, Session
from schemas.user import UserRegister, UserUpdate, UserOutput, User, Token, PasswordReset, PasswordResetRequest, DeleteAccountRequest
from auth_password import get_hashed_password, verify_password
from auth_token import (
    create_access_token,
    decode_access_token,
    get_current_user,
)  # , create_refresh_token
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from utils.notifications import send_password_reset_email

from database import Database
import os

db = Database(mode=os.getenv("ENV"))

router = APIRouter(
    prefix="/users",
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")

DbSession = Annotated[Session, Depends(db.get_session)]


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
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
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
async def login(session: DbSession, form_data: OAuth2PasswordRequestForm = Depends()):
    # Query the user based on email
    user = session.exec(select(User).where(User.email == form_data.username)).first()
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
async def verify(token: str, session: DbSession):
    payload = decode_access_token(token)
    uuid = payload.get("id")

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
async def users_update(user_id: int, user_update: UserUpdate, session: DbSession):
    user = session.get(User, user_id)
    if not user:
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
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")
    return user


@router.post("/forgot_password", status_code=status.HTTP_200_OK)
async def forgot_password(user_email: PasswordReset, session: DbSession):
    try:
        user = session.exec(select(User).where(User.email == user_email.email)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
                
        reset_token = create_access_token(data={"id": user.token_uuid}) # Generate a password reset token 
        reset_link = f"http://localhost:8001/reset_password?token={reset_token}"
        send_password_reset_email(user_email.email, reset_link)
        return {"detail": "Password reset email sent successfully"}
    except Exception as e:
        print(f"Error: {e} \n\n")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while sending the password reset email"
        )
         

@router.post("/reset_password", status_code=status.HTTP_200_OK)
async def reset_password(    
    reset_request: PasswordResetRequest, 
    session: DbSession, 
    current_user=Depends(get_current_user)
):
    try:
        if reset_request.new_password != reset_request.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password and confirm password do not match"
            )

        current_user.password_hash = get_hashed_password(reset_request.new_password)
        session.add(current_user)
        session.commit()
        session.refresh(current_user)
        return {"detail": "Password reset successful"}
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.delete("/delete")
async def delete_user(
    session: DbSession, 
    current_user=Depends(get_current_user)
):    
    try:
        session.delete(current_user)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting user")
    return {"detail": "User deleted successfully"} 