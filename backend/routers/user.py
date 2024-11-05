from fastapi import APIRouter, HTTPException, status #, Depends, Cookie
# from fastapi.responses import Response
from sqlmodel import SQLModel, select, Session
from schemas.user import UserRegister, UserLogin, UserOutput, User
from auth import get_hashed_password, verify_password, create_access_token, create_refresh_token

from database import Database
from datetime import timedelta
# from typing import Annotated

### USER ENDPOINTS ###
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
@router.post('/login')
async def login(request: UserLogin):
    try:
        with db.get_session() as session:

            # Query the user based on email
            user = session.exec(select(User).where(User.email == request.email)).first()
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User doesn't exist"
                )

            if not verify_password(user.password_hash, request.password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect password"
                )


            access_token_expires = timedelta(minutes=15)

            # Generate tokens
            access_token = create_access_token(
                data={"sub": str(user.id)},  # Token payload with user ID
                expires_delta=access_token_expires
            )
            refresh_token = create_access_token(
                data={"sub": str(user.id), "type": "refresh"},
                expires_delta=timedelta(days=30)  # Refresh token with a longer expiration
            )

            return {"access_token": access_token, "refresh_token": refresh_token}
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


'''
@router.get("/verify")
async def verify(token: str):
    with db.get_session() as session:
        payload = await decode_access_token(token=token, db=db)
        user = await models.User.find_by_id(db=db, id=payload[SUB])
    if not user:
        raise NotFoundException(detail="User not found")


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