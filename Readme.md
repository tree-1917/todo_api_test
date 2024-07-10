# FastAPI Todo App Tutorial 🚀

Welcome to the FastAPI Todo App! This tutorial will guide you through setting up and running your Todo App, as well as running tests and handling common warnings.

## Features ✨

- **CRUD Operations**: Create, Read, Update, and Delete todo items.
- **User Authentication**: Secure endpoints with JWT-based authentication.
- **Dependency Injection**: Properly manage database connections using dependency injection.
- **Documentation**: API documentation provided via FastAPI's built-in Swagger UI.

## Technologies Used 🛠️

- **FastAPI**: FastAPI framework for building APIs with Python.
- **SQLite**: Lightweight SQL database for storing todo items.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **SQLAlchemy**: Object-Relational Mapping (ORM) for Python.

## Project Structure 📁

Here's the structure of the project:

```text
TodoApp/
├── alembic/
├── alembic.ini
├── database.py
├── __init__.py
├── main.py
├── models.py
├── notes/
├── __pycache__/
├── pytest.ini
├── Readme.md
├── routers/
│   ├── admin.py
│   ├── auth.py
│   ├── __pycache__/
│   ├── todos.py
│   └── user.py
├── test/
│   ├── __init__.py
│   ├── __pycache__/
│   └── test_main.py
└── todosapp.db
```

## Setup Instructions 📋

### 1. **Clone the Repository**

First, clone the repository to your local machine:

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. **Install Dependencies**

Create a virtual environment and install the necessary dependencies:

```bash
python3 -m venv myenv
source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
pip install -r requirements.txt
```

### 3. **Run the Application**

Start the FastAPI application using `uvicorn`:

```bash
uvicorn main:app --reload
```

### 4. **Access API Documentation**

Open your browser and go to [http://localhost:8000/docs](http://localhost:8000/docs) to view and interact with the API using Swagger UI.

## API Endpoints 🚪

- **GET /todo/**: Retrieve all todo items.
- **GET /todo/{todo_id}/**: Retrieve a specific todo item by ID.
- **POST /todo/**: Create a new todo item.
- **PUT /todo/{todo_id}/**: Update an existing todo item.
- **DELETE /todo/{todo_id}/**: Delete a todo item.

## Running Tests 🧪

This project uses `pytest` for testing. To run the tests, use the following command:

```bash
pytest --disable-warnings
```

### Example Test

Here's an example test for the root endpoint:

```python
# TodoApp/test/test_main.py
from fastapi.testclient import TestClient
from main import app
from fastapi import status

client = TestClient(app)

def test_return_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"Message": "Welcome to Todo App V0.0"}
```

## Common Warnings and Fixes ⚠️

You may encounter warnings related to deprecated features in SQLAlchemy and Pydantic. Here are some common solutions:

### 1. **SQLAlchemy Warning**:

The warning indicates that `declarative_base()` is deprecated in SQLAlchemy 2.0 and should be replaced with `sqlalchemy.orm.declarative_base()`.

**Solution**:
Update your `database.py` to use the new import.

```python
# TodoApp/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base  # Updated import

SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # Updated usage
```

### 2. **Pydantic Warning**:

The warnings indicate that using extra keyword arguments on `Field` is deprecated in Pydantic V2.0 and should be replaced with `json_schema_extra`.

**Solution**:
Update the usage of `Field` in your models to use `json_schema_extra`.

```python
# TodoApp/models.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    phone_number: str

    class Config:
        json_schema_extra = {
            'username': {'min': 3},
            'email': {'min': 5},
            'full_name': {'min': 3, 'max': 100},
            'phone_number': {'min': 10, 'max': 15},
        }
```

## Contributing 🤝

Contributions are welcome! Please fork the repository and create a pull request with your improvements.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
