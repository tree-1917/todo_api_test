# TODO: Import necessary dependencies
from .utils import *
from ..routers.user import get_db, get_current_user
from fastapi import status

# TODO: Override get_db and get_current_user dependencies in app
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# TODO: Define test case to check user endpoint
def test_return_user(test_user):
    # Step 1: Send GET request to /user endpoint
    res = client.get("/user")
    
    # Step 2: Assert that response status code is 200 OK
    assert res.status_code == status.HTTP_200_OK
    
    # Step 3: Assert that response JSON matches expected values
    assert res.json()['username'] == "Hassan"  # TODO: Update assertion based on expected JSON response
    assert res.json()['email'] == "Hassan@xyz.com"
    assert res.json()['role'] == "admin"

# TODO: Define test case for successful password change
def test_change_password_success(test_user):
    res = client.put("/user/password", json={"password": "123", "new_password": "1234567"})
    
    assert res.status_code == status.HTTP_204_NO_CONTENT

# TODO: Define test case for invalid current password during password change
def test_change_password_invalid_current_password(test_user):
    res = client.put("/user/password", json={"password": "1323", "new_password": "1234567"})
    
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert res.json() == {"detail": "Error on password change"}

