# Tutorial: Testing as Part of SDLC with FastAPI

Testing is a crucial part of the Software Development Life Cycle (SDLC) that ensures software quality, reliability, and correctness. In this tutorial, we'll explore the importance of testing and demonstrate how to write and run tests for a FastAPI application.

### Why Testing? 🧪

Testing serves several critical purposes in software development:

- **Detecting Bugs Early**: Tests help identify bugs and issues in the code before they reach production.
- **Ensuring Quality**: Tests ensure that the software behaves as expected and meets the specified requirements.
- **Maintaining Confidence**: Automated tests provide confidence that changes and new features do not break existing functionality.
- **Supporting Refactoring**: Tests act as a safety net when refactoring code, ensuring that functionality remains intact.

### Types of Testing 📝

1. **Manual Testing** 🖐️:

   - Involves testing the application manually without using automated tools.
   - Useful for exploring user interfaces, usability testing, and ad-hoc scenarios.

2. **Unit Testing** 🧩:

   - Tests individual units or components of code in isolation.
   - Ensures that each part of the code works correctly on its own.

3. **Integration Testing** 🤝:
   - Tests interactions between various components/modules of the system.
   - Validates that different parts of the system work together as expected.

### Testing in FastAPI 🚀

FastAPI encourages and supports testing with tools like `pytest` and `TestClient`. Here's how you can set up and write tests for a FastAPI application.

### Example: FastAPI Application 🚀

Let's consider a simple FastAPI application that manages users:

```python
# main.py
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Fake database
class User(BaseModel):
    id: int
    username: str
    email: str

db = [
    User(id=1, username="alice", email="alice@example.com"),
    User(id=2, username="bob", email="bob@example.com"),
]

# API endpoints
@app.get("/users/", response_model=List[User])
async def read_users():
    return db

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    user = next((user for user in db if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@app.post("/users/", response_model=User)
async def create_user(user: User):
    db.append(user)
    return user
```

### Writing Tests 🛠️

#### 1. Install Dependencies

Ensure you have `pytest` and `requests` installed:

```bash
pip install pytest requests
```

#### 2. Write Unit Tests 🧪

Create a `tests` directory and add a test file `test_main.py`:

```python
# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2  # Assuming two initial users

def test_read_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == "alice"

def test_read_user_not_found():
    response = client.get("/users/10")
    assert response.status_code == 404

def test_create_user():
    new_user = {"id": 3, "username": "charlie", "email": "charlie@example.com"}
    response = client.post("/users/", json=new_user)
    assert response.status_code == 200
    assert response.json()["username"] == "charlie"
```

#### 3. Run Tests 🚀

Run the tests using `pytest`:

```bash
pytest
```

You should see output indicating the success or failure of each test.

### Conclusion ✨

Testing is essential for ensuring the quality and reliability of your FastAPI applications. By integrating testing into your SDLC, you can catch bugs early, maintain confidence in your codebase, and deliver high-quality software to users. FastAPI's support for testing with `pytest` and `TestClient` makes it easy to write comprehensive tests for your APIs. Integrate testing as a standard practice in your development workflow to build robust and reliable applications.
