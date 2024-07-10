from .utils import *
from ..routers.auth import get_db, _auth_user, _create_access_token, SECRET_KEY, ALG, get_current_user
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

# TODO: Override get_db dependency in app
app.dependency_overrides[get_db] = override_get_db

# TODO: Define test case for authentication
def test_auth_user(test_user):
    db = TestingSessionLocal()
    
    # Step 1: Authenticate with correct username and password
    auth_user = _auth_user(test_user.username, "123", db)
    
    # Step 2: Assert that authentication is successful
    assert auth_user is not None
    assert auth_user.username == test_user.username
    
    # Step 3: Attempt to authenticate with non-existent username
    non_existent_user = _auth_user("Wrong User Name", "123", db)
    
    # Step 4: Assert that authentication fails for non-existent user
    assert non_existent_user is False

    # Step 5: Attempt to authenticate with correct username but wrong password
    wrong_password_user = _auth_user(test_user.username, "123123", db)
    
    # Step 6: Assert that authentication fails for wrong password
    assert wrong_password_user is False
    
    
# TODO: Define test case for creating an access token
def test_create_access_token(test_user):
    username = "hassan"
    user_id = 1
    role = "user"
    expires_delta = timedelta(days=1)
    
    token = _create_access_token(username, user_id, role, expires_delta)
    
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALG], options={"verify_signature": False})
    
    # TODO: Assert decoded token attributes match expected values
    assert decoded_token["username"] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role    


# TODO: Define test case for validating token and getting current user
@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {"username": "Hassan", 'id': 1, "role": "admin"}
    
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALG)
    
    user = await get_current_user(token=token)
    
    # TODO: Assert that the returned user data matches expected values
    assert user == {"username": "Hassan", "id": 1, "user_role": "admin"}  # Update based on actual returned data


# TODO: Define test case for handling missing payload in token
@pytest.mark.asyncio 
async def test_get_current_user_missing_payload():
    encode = {"role": "user"}
    
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALG)
    
    # TODO: Expect an HTTPException to be raised due to missing payload
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)
        
    # TODO: Assert the exception status code and detail message
    assert excinfo.value.status_code == 401 
    assert excinfo.value.detail == "Could not validate user."