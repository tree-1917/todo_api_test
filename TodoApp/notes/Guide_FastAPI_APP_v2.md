# Step-by-Step Guide to Adding User Login with JWT Authentication 🛠️🚀

## Step 1: Install Additional Dependencies

If you haven't already installed `python-jose`, you can add it to your `requirements.txt`:

```text
python-jose
```

Install the dependencies:

```bash
pip install python-jose
```

## Step 2: Update Pydantic Schemas

Update `schemas.py` to include login-related schemas and token data.

> **schemas.py**

```python
# schemas.py

from pydantic import BaseModel
from typing import List, Optional

class TodoBase(BaseModel):
    title: str
    description: str
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoInDB(TodoBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    todos: List[TodoInDB] = []

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
```

## Step 3: Utility Functions for Password Hashing and JWT

Create utility functions for hashing passwords and creating/verifying JWTs.

> **utils.py**

```python
# utils.py

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "secret_key"  # Replace with a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise JWTError
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

## Step 4: Update the Auth Router

Update the `auth.py` file to include the login endpoint.

> **auth.py**

```python
# routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from utils import get_password_hash, verify_password, create_access_token
from database import get_db
from models import User
from schemas import UserCreate, UserLogin, UserInDB, Token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register/", response_model=UserInDB)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login/", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Dependency to get the current user
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    username = decode_access_token(token)
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## Step 5: Protect Endpoints with JWT Authentication

Update the `todos.py` to protect the endpoints with JWT authentication.

> **todos.py**

```python
# routers/todos.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Todo, User
from schemas import TodoCreate, TodoInDB
from typing import List
from routers.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=TodoInDB)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        owner_id=current_user.id
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/", response_model=List[TodoInDB])
def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todos = db.query(Todo).filter(Todo.owner_id == current_user.id).offset(skip).limit(limit).all()
    return todos

@router.get("/{todo_id}", response_model=TodoInDB)
def read_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == current_user.id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=TodoInDB)
def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == current_user.id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == current_user.id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
```

## Step 6: Run the Application

Run your FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload
```

Open your browser and go to `http://127.0.0.1:8000`. You should see a welcome message.

## Summary 📝

In this tutorial, we added a login endpoint to the FastAPI application using JWT authentication. We created utility functions for password hashing and JWT handling, updated the `auth.py` file to include registration and login endpoints, and protected the `todos.py` endpoints using JWT authentication.

This approach provides a secure and scalable authentication system for your FastAPI application. Happy coding! 🚀
