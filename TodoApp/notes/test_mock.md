# Mocking in FastAPI Project: A Tutorial 🚀

In this tutorial, we'll explore how to use mocking in a FastAPI project to test your application components in isolation. Mocking is particularly useful for unit testing when you want to replace real dependencies with simulated ones.

#### 1. Setting Up the Project 🛠️

First, let's create a basic FastAPI project. Make sure you have `fastapi` and `uvicorn` installed. You can install them using pip:

```bash
pip install fastapi uvicorn
```

Create a file named `main.py`:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Invalid item ID")
    return {"item_id": item_id, "name": f"Item {item_id}"}
```

Run the FastAPI app using `uvicorn`:

```bash
uvicorn main:app --reload
```

#### 2. Installing Testing Dependencies 🧩

For testing, we'll use `pytest` and `httpx`. Additionally, we'll use `unittest.mock` for mocking.

```bash
pip install pytest httpx
```

#### 3. Creating Test File 📄

Create a file named `test_main.py` for writing your tests.

#### 4. Writing Basic Test 📜

First, let's write a basic test without mocking to understand the structure. Add the following to `test_main.py`:

```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_read_item():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "name": "Item 1"}
```

Run the test using `pytest`:

```bash
pytest test_main.py
```

#### 5. Introducing Mocking 🧪

Suppose the `read_item` function calls an external API or service. We want to mock this external call to isolate our tests.

First, let's modify our `main.py` to include a dependency that we can mock:

```python
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()

def get_item_name(item_id: int):
    return f"Item {item_id}"

@app.get("/items/{item_id}")
async def read_item(item_id: int, name: str = Depends(get_item_name)):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Invalid item ID")
    return {"item_id": item_id, "name": name}
```

Now, in `test_main.py`, we will mock the `get_item_name` function.

```python
from unittest.mock import patch

@pytest.mark.asyncio
async def test_read_item_mocked():
    with patch("main.get_item_name") as mock_get_item_name:
        mock_get_item_name.return_value = "Mocked Item"
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/items/1")
        assert response.status_code == 200
        assert response.json() == {"item_id": 1, "name": "Mocked Item"}
```

Here, `patch` is used to replace `get_item_name` with a mock that returns "Mocked Item".

#### 6. Running Mocked Tests 🏃‍♂️

Run the tests using `pytest`:

```bash
pytest test_main.py
```

You should see that both tests pass, demonstrating how to use mocking to isolate parts of your FastAPI application during testing.

#### 7. Conclusion 🎉

Using mocking in FastAPI projects allows you to isolate and test components without relying on actual external dependencies. This ensures your tests are fast, reliable, and focus on the unit of code being tested.

With this tutorial, you should have a good understanding of how to set up and use mocks in your FastAPI project. If you have any questions or need further examples, feel free to ask!
