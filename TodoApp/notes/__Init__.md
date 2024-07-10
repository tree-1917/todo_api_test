# 🎓 Tutorial: Using `__init__.py` in Your Project

### 📚 What is `__init__.py`?

The `__init__.py` file is used to mark a directory as a Python package. This allows you to organize your code into modules and sub-packages, enabling cleaner imports and better structure.

### 🤔 Why Use `__init__.py`?

1. **📦 Mark a directory as a package**: Allows Python to treat the directory as a package.
2. **🔄 Initialization code**: Code in `__init__.py` runs when the package is imported.
3. **🎯 Explicit imports**: Control what is imported when `from package import *` is used.
4. **📂 Sub-package imports**: Simplify importing sub-packages or modules.
5. **🛠️ Path management**: Modify the package’s `__path__`.
6. **📜 Package-level documentation**: Provide docstrings for the package.
7. **🆕 Versioning**: Define a version for the package.

### 🚀 Converting a Directory to a Package

To convert a directory to a package, simply add an empty `__init__.py` file to it.

```bash
touch your_directory/__init__.py
```

### 🛠️ Example Usage in Your Project

Let’s assume your project structure is as follows:

```
TodoApp/
├── alembic/
├── __init__.py
├── main.py
├── alembic.ini
├── models.py
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── todos.py
│   ├── admin.py
│   └── user.py
├── database.py
├── notes/
├── test/
│   ├── __init__.py
│   └── test_main.py
└── todosapp.db
```

### 📋 Step-by-Step Guide

1. **📝 Create `__init__.py` in the Root Directory**

   In the root directory `TodoApp/`, create `__init__.py`.

   ```python
   # TodoApp/__init__.py
   """
   TodoApp: A sample Todo Application using FastAPI.
   """

   # Import necessary sub-packages or modules
   from . import main, models, database, routers

   # Versioning
   __version__ = '1.0.0'
   ```

2. **📝 Create `__init__.py` in the `routers` Directory**

   In the `routers/` directory, create `__init__.py`.

   ```python
   # TodoApp/routers/__init__.py
   from fastapi import APIRouter

   # Create a main router
   api_router = APIRouter()

   # Import and include sub-routers
   from . import auth, todos, admin, user

   api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
   api_router.include_router(todos.router, prefix="/todos", tags=["todos"])
   api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
   api_router.include_router(user.router, prefix="/user", tags=["user"])
   ```

3. **📝 Modify `main.py` to Use the Router**

   Modify `main.py` to include the main router from the `routers` package.

   ```python
   # TodoApp/main.py
   from fastapi import FastAPI
   from .routers import api_router

   app = FastAPI()

   app.include_router(api_router)

   @app.get("/")
   async def read_root():
       return {"Message": "Welcome to Todo App V0.0"}
   ```

4. **📝 Define Models**

   Define your models in `models.py`.

   ```python
   # TodoApp/models.py
   from sqlalchemy import Column, Integer, String
   from .database import Base

   class User(Base):
       __tablename__ = 'users'
       id = Column(Integer, primary_key=True, index=True)
       username = Column(String, unique=True, index=True)
       email = Column(String, unique=True, index=True)
       full_name = Column(String)
       phone_number = Column(String)
   ```

5. **📝 Create an Empty `__init__.py` in the `test` Directory**

   In the `test/` directory, create an empty `__init__.py` file.

   ```python
   # TodoApp/test/__init__.py
   ```

6. **📝 Create Tests**

   Create a test file in the `test/` directory.

   ```python
   # TodoApp/test/test_main.py
   from fastapi.testclient import TestClient
   from fastapi import status
   from TodoApp.main import app

   client = TestClient(app)

   def test_return_root():
       response = client.get("/")
       assert response.status_code == status.HTTP_200_OK
       assert response.json() == {"Message": "Welcome to Todo App V0.0"}
   ```

7. **🧪 Run Tests**

   Navigate to the root directory `TodoApp/` and run:

   ```bash
   pytest
   ```

By following these steps, you ensure that your project is well-structured and that imports are handled correctly. The `__init__.py` files allow you to organize your code into manageable packages, making your project easier to maintain and extend.

### Summary

- 📦 `__init__.py` marks a directory as a package.
- 📝 It can contain initialization code, control imports, and manage package documentation and versioning.
- 🚀 Use `__init__.py` in various directories to create a well-structured, maintainable project.
