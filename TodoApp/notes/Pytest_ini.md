# Setting Up `pytest` for FastAPI Projects

#### Step 1: Install `pytest` and Required Dependencies

Make sure you have `pytest` installed in your Python environment:

```bash
pip install pytest
```

If you are using FastAPI, you might also need `fastapi.testclient` for testing API endpoints:

```bash
pip install fastapi[all]
```

#### Step 2: Project Structure

Assume you have a typical FastAPI project structure:

```
project-root/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── user.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── todos.py
│   ├── database.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_admin.py
│   ├── test_users.py
│   ├── test_main.py
│   ├── test_todos.py
│
├── pytest.ini
├── requirements.txt
└── README.md
```

- **`app/`**: Contains your FastAPI application code.
- **`tests/`**: Directory for your test files.
- **`pytest.ini`**: Configuration file for `pytest`.
- **`requirements.txt`**: Dependencies file for your project.

#### Step 3: `pytest.ini` Configuration

Create or update `pytest.ini` in your project root with the following configuration:

```ini
[pytest]
# Additional command line options
addopts =
    -ra  # Show extra test summary info for failed and skipped tests
    --disable-warnings  # Disable all warnings during test execution

# Test discovery
python_files = test_*.py  # Look for files starting with 'test_' and ending with '.py'
testpaths = tests  # Directory or directories to search for tests

# Logging configuration
log_cli = true  # Show log output on the console during test runs
log_cli_level = INFO  # Set log level to INFO for console output

# Test result display
console_output_style = progress  # Use 'progress' style for console output

# Coverage configuration (if coverage is used)
[coverage]
omit =
    */myenv/*  # Exclude virtual environment files from coverage
    */tests/*  # Exclude test files from coverage

# Marker configuration
[pytest.markers]
slow: Tests that are slow to run 🐢
fast: Tests that are fast to run 🚀

# Test session debugging
pdbcls = pdb.Pdb  # Use the standard Python debugger for interactive debugging

# pytest-django plugin configuration (if using Django)
# Add Django specific configuration here if applicable

# Disable warnings globally (optional)
filterwarnings =
    ignore::DeprecationWarning  # Ignore DeprecationWarnings globally
```

#### Step 4: Writing Tests

Here's an example of a test file (`test_admin.py`) using `pytest` for your FastAPI application:

```python
# tests/test_admin.py

import pytest
from fastapi.testclient import TestClient
from fastapi import status
from ..app.main import app  # Adjust import paths as per your project structure

client = TestClient(app)

@pytest.fixture
def test_todo():
    # Replace with actual test data setup for Todos if needed
    yield

# Example test cases
def test_admin_read_all_auth(test_todo):
    res = client.get("/admin/todo")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == [{
        "complete": False,
        "title": "learn to code",
        "description": "need to learn everyday!",
        "priority": 3,
        "id": 1,
        "owner_id": 1
    }]

def test_admin_delete_todo(test_todo):
    res = client.delete("/admin/todo/1")
    assert res.status_code == status.HTTP_204_NO_CONTENT

    # Example to verify deletion from database
    # Replace with actual database check code
    # db = TestingSessionLocal()
    # model = db.query(Todos).filter(Todos.id == 1).first()
    # assert model is None

# Add more tests as needed for different endpoints and scenarios
```

#### Step 5: Running Tests

Run `pytest` from your project root directory:

```bash
pytest
```

This will execute all tests in the `tests/` directory according to the configuration specified in `pytest.ini`. Adjust and expand your tests and configuration as your project grows!

#### Conclusion

Setting up `pytest` for FastAPI projects involves configuring `pytest.ini`, organizing tests in the `tests/` directory, and using fixtures and markers for better test management. With this setup, you can effectively test your FastAPI application with confidence.
