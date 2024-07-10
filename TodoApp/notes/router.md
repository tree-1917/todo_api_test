# FastAPI Routers Tutorial 🛠️🚀

## Step 1: Install FastAPI and Uvicorn

First, you need to install FastAPI and an ASGI server, such as Uvicorn.

```bash
pip install fastapi
pip install uvicorn
```

## Step 2: Create the Main Application File

Create a file called `main.py`. This file will serve as the entry point for your FastAPI application.

```python
# main.py

from fastapi import FastAPI
from routers import items, users

app = FastAPI()

# Include routers
app.include_router(items.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application! 🎉"}
```

## Step 3: Create Routers Directory and Files

Create a directory called `routers`. Inside this directory, create two files: `items.py` and `users.py`.

```bash
mkdir routers
touch routers/items.py routers/users.py
```

## Step 4: Define Routes in the Routers

Let's define some routes in `items.py` and `users.py`.

> **items.py**

```python
# routers/items.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/items/")
def read_items():
    return [{"item_id": "foo"}, {"item_id": "bar"}]

@router.get("/items/{item_id}")
def read_item(item_id: str):
    return {"item_id": item_id, "description": "This is an item."}
```

> **users.py**

```python
# routers/users.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/users/")
def read_users():
    return [{"username": "alice"}, {"username": "bob"}]

@router.get("/users/{username}")
def read_user(username: str):
    return {"username": username, "message": "This is a user."}
```

## Step 5: Run the Application

Run your FastAPI application using Uvicorn.

```bash
uvicorn main:app --reload
```

Open your browser and go to `http://127.0.0.1:8000`. You should see a welcome message.

## Step 6: Test the Endpoints

Now, let's test the endpoints we created:

- `http://127.0.0.1:8000/items/`
- `http://127.0.0.1:8000/items/{item_id}`
- `http://127.0.0.1:8000/users/`
- `http://127.0.0.1:8000/users/{username}`

### Summary 📝

In this tutorial, we learned how to create a FastAPI application with routers to organize our code better. We created two routers, `items` and `users`, and included them in our main application.

FastAPI routers help to keep your code modular and organized, especially as your application grows. Enjoy building with FastAPI! 🎉🚀
