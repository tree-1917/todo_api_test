from fastapi.testclient import TestClient as tc 
from ..main import app
from fastapi import status 


client = tc(app)


def test_return_root(): 
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK 
    assert response.json() == {"Message" : "Welcome to Todo App V0.0"}
    