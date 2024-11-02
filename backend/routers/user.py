from fastapi import APIRouter, HTTPException
from schemas.user import UserBase, UserCreate, UserGet, UserUpdate, UserOutput, UserLogin, User
from sqlmodel import SQLModel, select, session

router = APIRouter(
    prefix="/users",
)

### USER ENDPOINTS ###

# Registers new user
@app.post("/user/register", response_model=UserOutput, status_code=201)
async def create_user(user: UserCreate):
    hashed_password = get_hashed_password(user.password)
    print(f"password: {hashed_password} \n")
    new_user = User(email=user.email, password_hash=hashed_password)
    with db.get_session() as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    return UserOutput(email=new_user.email, username=user.username)

# Authenticates existing user
@app.post('login')
async def login(request: UserLogin):
    print(f"password: {request.password}")
    print(f"request email: {request.email}")
    with db.get_session() as session:
        user = session.exec(select(User).where(User.email == request.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User doesn't exist"
        )
    if not verify_password(user.password_hash, request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "email": user.email}

# Sends a Url to reset User's password
@app.post("forget-password")
async def forget_password(request: )
    user = get_user_by_email(db, request.user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
                detail="User doesn't exist"
        )
        
    access_token = create_access_token(data={"sub": user.email})
    await send_reset_password(recipient=user.email, user=user, url=url, expirae=RESET_TOKEN_EXPIRE)

        
# Get user details by ID
@app.get("{user_id}", response_model=UserOutput)
async def get_user(user_id: int):
    with db.get_session() as session:
        user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No User Found")
    return userOutput(email=user.email)


# Update user details by id
@app.put("/users/{user_id}", response_model=UserGet)
async def users_update(user_id: int, user_update: UserUpdate):
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
@app.delete("/users/{user_id}", response_model=UserGet)
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

# Get a user by id
@app.get("/users/{user_id}", response_model=UserGet)
async def users_get(user_id: int):
    with db.get_session() as session:
        user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user details by id
@app.put("/users/{user_id}", response_model=UserGet)
async def users_update(user_id: int, user_update: UserUpdate):
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
@app.delete("/users/{user_id}", response_model=UserGet)
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

def get_user_by_email(db: Session = Depends(get_db), email: str):
    user = session.exec(select(User).where(User.email == email)).first()
    return user