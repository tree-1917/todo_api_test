s# Pytest - Setup Dependencies Tutorial 📚

In this tutorial, we will go through the steps to set up dependencies using pytest in Python. This is crucial for creating a clean and maintainable test suite. We'll cover the basics of pytest fixtures, which allow you to set up and tear down dependencies for your tests.

#### 1. Installation 📥

First, make sure you have pytest installed. You can install it using pip:

```bash
pip install pytest
```

#### 2. Basic Test Structure 🧩

Let's start with a basic test to understand the structure. Create a file named `test_example.py` with the following content:

```python
def test_example():
    assert 1 + 1 == 2
```

You can run this test using the following command:

```bash
pytest test_example.py
```

#### 3. Using Fixtures 🛠️

Fixtures are a powerful feature of pytest that allow you to set up and tear down resources that your tests depend on.

##### Example: Simple Fixture 🌟

Create a fixture to provide some sample data for your tests. Add the following to `test_example.py`:

```python
import pytest

@pytest.fixture
def sample_data():
    return {"key1": "value1", "key2": "value2"}

def test_sample_data(sample_data):
    assert sample_data["key1"] == "value1"
    assert sample_data["key2"] == "value2"
```

In this example, `sample_data` is a fixture that provides a dictionary for the test `test_sample_data`.

#### 4. Using Fixtures for Setup and Teardown 🏗️🧹

You can also use fixtures to set up and tear down resources, such as database connections or temporary files.

##### Example: Database Connection 💾

Let's say we want to set up a database connection for our tests. Create a file named `test_database.py`:

```python
import pytest

class DatabaseConnection:
    def __init__(self):
        self.connected = False

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

@pytest.fixture
def db_connection():
    connection = DatabaseConnection()
    connection.connect()
    yield connection
    connection.disconnect()

def test_db_connection(db_connection):
    assert db_connection.connected
```

In this example, the `db_connection` fixture sets up a database connection before the test and tears it down after the test using the `yield` statement.

#### 5. Using Multiple Fixtures 🔀

You can use multiple fixtures in a single test by passing them as arguments to the test function.

##### Example: Multiple Fixtures 🌐

Create another file named `test_multiple_fixtures.py`:

```python
import pytest

@pytest.fixture
def sample_data():
    return {"key1": "value1", "key2": "value2"}

@pytest.fixture
def db_connection():
    connection = DatabaseConnection()
    connection.connect()
    yield connection
    connection.disconnect()

def test_multiple_fixtures(sample_data, db_connection):
    assert sample_data["key1"] == "value1"
    assert db_connection.connected
```

#### 6. Fixture Scope 🏠

By default, fixtures are created and destroyed for each test function. You can change the fixture scope using the `scope` parameter.

##### Example: Fixture Scope 🔄

```python
@pytest.fixture(scope="module")
def db_connection():
    connection = DatabaseConnection()
    connection.connect()
    yield connection
    connection.disconnect()
```

Available scopes are:

- `function` (default): The fixture is set up and destroyed for each test function.
- `class`: The fixture is set up and destroyed once per test class.
- `module`: The fixture is set up and destroyed once per module.
- `session`: The fixture is set up and destroyed once per session.

#### 7. Parametrizing Fixtures 🎛️

You can also parametrize fixtures to run tests with different configurations.

##### Example: Parametrizing Fixtures 🎯

```python
@pytest.fixture(params=[1, 2, 3])
def number(request):
    return request.param

def test_number(number):
    assert number in [1, 2, 3]
```

In this example, the test `test_number` will run three times, once for each value in the `params` list.

#### 8. Conclusion 🎉

Using pytest fixtures allows you to manage your test dependencies efficiently and makes your tests more readable and maintainable. Here is a summary of what we've covered:

- Basic test structure
- Creating and using fixtures
- Setting up and tearing down resources
- Using multiple fixtures in a test
- Changing fixture scope
- Parametrizing fixtures

With these basics, you should be able to set up and manage dependencies in your pytest test suite effectively.
