import logging
from ..routers.todos import get_db, get_current_user
from fastapi import status
from ..models import Todos
from .utils import *

# TODO: Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# TODO: Apply the dependency overrides to the FastAPI app
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


# TODO: Define a test function to test the /todo endpoint with authentication
def test_read_all_auth(test_todo):
    # TODO: Log a custom message
    logger.info("Hello from test_read_all_auth")

    # TODO: Send a GET request to the /todo endpoint
    response = client.get("/todo")

    # TODO: Ensure the response status is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # TODO: Assert the response JSON matches the expected output
    assert response.json() == [{
        "complete": False,
        "title": "learn to code",
        "description": "need to learn everyday!",
        "priority": 3,
        "id": 1,
        "owner_id": 1
    }]

# TODO: Define a test function to test the /todo/1 endpoint with authentication
def test_read_one_auth(test_todo):
    # TODO: Log a custom message
    logger.info("Hello from test_read_one_auth")

    # TODO: Send a GET request to the /todo/1 endpoint
    response = client.get("/todo/1")

    # TODO: Ensure the response status is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # TODO: Assert the response JSON matches the expected output
    assert response.json() == {
        "complete": False,
        "title": "learn to code",
        "description": "need to learn everyday!",
        "priority": 3,
        "id": 1,
        "owner_id": 1
    }

# TODO: Define a test function to handle not found cases
def test_read_one_auth_not_found(test_todo):
    # TODO: Log a custom message
    logger.info("Hello from test_read_one_auth_not_found")

    # TODO: Send a GET request to the /todo/999 endpoint
    response = client.get("/todo/999")
    
    # TODO: Ensure the response status is 404 Not Found
    assert response.status_code == 404
    
    # TODO: Assert the response JSON matches the expected output
    assert response.json() == {"detail": "Todo not found."}

# TODO: Define a test function to test creating a new todo item
def test_create_todo(test_todo):
    # TODO: Log a custom message
    logger.info("Hello from test_create_todo")

    # TODO: Define the request payload for creating a new todo
    request_data = {
        "title": "New todo",
        "description": "this is new todo",
        "priority": 3,
        "complete": False
    }
    
    # TODO: Send a POST request to the /todo/ endpoint
    response = client.post("/todo/", json=request_data)
    
    # TODO: Ensure the response status is 201 Created
    assert response.status_code == 201

    # TODO: Log the response JSON
    logger.info(f"Response JSON: {response.json()}")

    # TODO: Assert the response JSON contains the success message
    assert response.json().get("Message") == "Added New Todo Item Successfully"
    
    # TODO: Send a GET request to verify the todo item was created
    response = client.get("/todo/2")
    
    # TODO: Ensure the response status is 200 OK
    assert response.status_code == status.HTTP_200_OK
    
    # TODO: Assert the response JSON matches the expected output
    assert response.json() == {
        "complete": False,
        "title": "New todo",
        "description": "this is new todo",
        "priority": 3,
        "id": 2,  
        "owner_id": 1
    }

# TODO: Define a test function to test updating an existing todo item
def test_update_todo_found(test_todo):
    # TODO: Log a custom message
    logger.info("Hello from test_update_todo_found")
    
    # TODO: Define the request payload for updating the todo
    request_data = {
        "title": "Change the title of the todo already saved!",
        "description": "Need to learn everyday!",
        "priority": 3,
        "complete": False  # Corrected key to match expected field
    }

    # TODO: Send a PUT request to the /todo/1 endpoint
    res = client.put("/todo/1", json=request_data)
    
    # TODO: Ensure the response status is 204 No Content
    assert res.status_code == 204
    
    # TODO: Verify the todo item was updated in the database
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "Change the title of the todo already saved!"

# TODO: Define a test function to handle not found cases for updating
def test_update_todo_not_found(test_todo):
    # TODO: Log a custom message
    logger.info("Hello from test_update_todo_not_found")
    
    # TODO: Define the request payload for updating the todo
    request_data = {
        "title": "Non-existent todo",
        "description": "This todo does not exist",
        "priority": 1,
        "complete": False
    }

    # TODO: Send a PUT request to the /todo/999 endpoint
    res = client.put("/todo/999", json=request_data)
    
    # TODO: Ensure the response status is 404 Not Found
    assert res.status_code == 404
    
    # TODO: Assert the response JSON matches the expected output
    assert res.json() == {"detail": "Todo not found."}

# TODO: Define a test function to test deleting a todo item
def test_delete_todo(test_todo):
    # Send a DELETE request to the /todo/1 endpoint
    response = client.delete("/todo/1")
    
    # Ensure the response status is 204 No Content
    assert response.status_code == 204
    
    # Verify the todo item was deleted from the database
    db = TestingSessionLocal() 
    
    # Attempt to retrieve the todo item with id 1 from the database
    # and assert that it does not exist
    model = db.query(Todos).filter(Todos.id == 1).first() 
    
    assert model is None


# TODO: Define a test function to test deleting a todo item
def test_delete_todo_not_found(test_todo):
    # Send a DELETE request to the /todo/1 endpoint
    response = client.delete("/todo/999")
    
    # Ensure the response status is 204 No Content
    assert response.status_code == 404
    assert response.json() == {"detail" : "Todo not found."}