# Tutorial: Using pytest to Test FastAPI APIs 🚀

In this tutorial, we will cover how to use `pytest` to test APIs built with FastAPI. We will also explore the use of `@pytest.fixture` and other decorators to enhance our tests.

### Step 1: Setting Up the Project 🛠️

1. **Install FastAPI and uvicorn**:

   ```bash
   pip install fastapi uvicorn
   ```

2. **Create a simple FastAPI app** (`main.py`):

   ```python
   from fastapi import FastAPI, HTTPException

   app = FastAPI()

   users_db = {"alice": {"name": "Alice", "age": 25}, "bob": {"name": "Bob", "age": 30}}

   @app.get("/users/{username}")
   async def get_user(username: str):
       user = users_db.get(username)
       if user:
           return user
       raise HTTPException(status_code=404, detail="User not found")
   ```

### Step 2: Setting Up pytest 🔧

1. **Install pytest and pytest-asyncio**:

   ```bash
   pip install pytest pytest-asyncio
   ```

2. **Create a pytest configuration file** (`pytest.ini`):
   ```ini
   [pytest]
   addopts = --disable-warnings
   ```

### Step 3: Writing Tests with pytest ✍️

1. **Create a test file** (`test_main.py`):

   ```python
   import pytest
   from fastapi.testclient import TestClient
   from main import app

   client = TestClient(app)

   @pytest.fixture
   def sample_user():
       return {"username": "alice", "name": "Alice", "age": 25}

   def test_get_user(sample_user):
       response = client.get(f"/users/{sample_user['username']}")
       assert response.status_code == 200
       assert response.json() == sample_user

   def test_get_nonexistent_user():
       response = client.get("/users/nonexistent")
       assert response.status_code == 404
       assert response.json() == {"detail": "User not found"}
   ```

### Step 4: Running the Tests 🏃

Run the tests using the following command:

```bash
pytest
```

### Using `@pytest.fixture` 🧩

`@pytest.fixture` is used to create reusable components that can be shared across multiple tests. It helps in setting up preconditions needed for tests.

**Example with `@pytest.fixture`**:

```python
@pytest.fixture
def sample_user():
    return {"username": "alice", "name": "Alice", "age": 25}

def test_get_user(sample_user):
    response = client.get(f"/users/{sample_user['username']}")
    assert response.status_code == 200
    assert response.json() == sample_user
```

### Using Additional `pytest` Decorators 🎨

#### `@pytest.mark.parametrize`

`@pytest.mark.parametrize` allows you to run a test with multiple sets of parameters.

**Example with `@pytest.mark.parametrize`**:

```python
@pytest.mark.parametrize("username,expected_status", [
    ("alice", 200),
    ("bob", 200),
    ("nonexistent", 404),
])
def test_get_user(username, expected_status):
    response = client.get(f"/users/{username}")
    assert response.status_code == expected_status
```

#### `@pytest.fixture(scope="module")`

You can specify the scope of a fixture to control its lifetime. For example, using `scope="module"` means the fixture is set up once per module.

**Example with `scope="module"`**:

```python
@pytest.fixture(scope="module")
def module_sample_user():
    return {"username": "alice", "name": "Alice", "age": 25}

def test_get_user(module_sample_user):
    response = client.get(f"/users/{module_sample_user['username']}")
    assert response.status_code == 200
    assert response.json() == module_sample_user
```

### Conclusion 🎉

Using `pytest` with FastAPI allows you to write clean and maintainable tests for your APIs. Fixtures and decorators like `@pytest.fixture` and `@pytest.mark.parametrize` help to keep your tests DRY (Don't Repeat Yourself) and organized.

### Common `pytest` Commands 📝

| Command                     | Description                                          |
| --------------------------- | ---------------------------------------------------- |
| `pytest`                    | Run all tests in the project                         |
| `pytest -v`                 | Run tests with verbose output                        |
| `pytest <file>`             | Run tests from a specific file                       |
| `pytest -k "name"`          | Run tests with names that match the given expression |
| `pytest --maxfail=1`        | Stop after the first failure                         |
| `pytest --disable-warnings` | Disable warnings during test run                     |

By following this tutorial, you should now have a solid foundation for testing your FastAPI applications with `pytest`. Happy testing! 🎊
