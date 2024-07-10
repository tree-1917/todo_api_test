# Step-by-Step Guide to Creating a FastAPI Application 🛠️🚀

## Step 1: Project Structure

First, create a directory for your project and set up the following structure:

```text
fastapi_project/
├── main.py
├── database.py
├── models.py
├── routers/
│   ├── todos.py
│   └── auth.py
└── requirements.txt
```

## Step 2: Install Dependencies

Create a `requirements.txt` file and add the necessary dependencies:

```text
fastapi
uvicorn
sqlalchemy
databases
pydantic
passlib[bcrypt]
python-jose
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Step 3: Set Up the Database

Create a `database.py` file to configure the database connection:

```python
# database.py

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from databases import Database

DATABASE_URL = "sqlite:///./test.db"  # Replace with your database URL

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
Base = declarative_base()
```

## Step 4: Create Models

Create a `models.py` file to define the database models:

```python
# models.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")
```

## Step 5: Create Routers

Create a `routers/` directory and add two files: `todos.py` for CRUD operations and `auth.py` for authentication.

> **todos.py**

```python
# routers/todos.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import database, engine
from models import Todo
from pydantic import BaseModel

router = APIRouter()

class TodoCreate(BaseModel):
    title: str
    description: str
    completed: bool

@router.post("/todos/", response_model=TodoCreate)
async def create_todo(todo: TodoCreate, db: Session = Depends(database)):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/todos/")
async def read_todos(skip: int = 0, limit: int = 10, db: Session = Depends(database)):
    todos = db.query(Todo).offset(skip).limit(limit).all()
    return todos

@router.get("/todos/{todo_id}")
async def read_todo(todo_id: int, db: Session = Depends(database)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/todos/{todo_id}", response_model=TodoCreate)
async def update_todo(todo_id: int, todo: TodoCreate, db: Session = Depends(database)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(database)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}
```

> **auth.py**

```python
# routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import database, engine
from models import User
from pydantic import BaseModel

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/register/")
async def register_user(user: UserCreate, db: Session = Depends(database)):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}
```

## Step 6: Set Up Main Application

Create the `main.py` file to set up the FastAPI application and include the routers:

```python
# main.py

from fastapi import FastAPI
from database import database, engine, Base
from routers import todos, auth

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include the routers
app.include_router(todos.router)
app.include_router(auth.router)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application! 🎉"}
```

## Step 7: Run the Application

Run your FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload
```

Open your browser and go to `http://127.0.0.1:8000`. You should see a welcome message.

### Summary 📝

In this tutorial, we created a professional FastAPI application with a structured project layout. We set up a database, created models, and implemented routers for CRUD operations and authentication. This approach helps in keeping the code modular, maintainable, and scalable. 🚀

---
