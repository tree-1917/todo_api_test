from .utils import * 
from ..routers.admin import get_db, get_current_user 
from fastapi import status
from ..models import Todos

# Dependency overrides for testing purposes
app.dependency_overrides[get_db] = override_get_db 
app.dependency_overrides[get_current_user] = override_get_current_user

# TODO: Implement test case for admin read all todos endpoint
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

# TODO: Implement test case for admin delete todo endpoint
def test_admin_delete_todo(test_todo):
    res = client.delete("/admin/todo/1")
    
    assert res.status_code == 204 
    
    # Verify that the todo item is deleted from the database
    db = TestingSessionLocal() 
    model = db.query(Todos).filter(Todos.id == 1).first() 
    assert model is None  # Ensure the todo item is deleted
    
    
def test_admin_delet_todo_not_found(test_todo): 
    res = client.delete("/admin/todo/999")
    assert res.status_code == 404 
    assert res.json() == {"detail" : "Todo Not Found"}