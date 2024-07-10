# == Import necessary libraries ==
# TODO 1: Import necessary libraries from typing and Pydantic
from typing import Annotated
from pydantic import BaseModel, Field
# TODO 2: Import necessary modules from SQLAlchemy and FastAPI
from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

# TODO 3: Import the Todos model
from ..models import Users
# TODO 4: Import database connection details (engine and session factory)
from ..database import SessionLocal
from passlib.context import CryptContext
from .auth import get_current_user 

# TODO 5: Create an instance of APIRouter with prefix and tags
router = APIRouter(
    prefix="/user",
    tags=["user"]
)

# TODO 6: Define a dependency function to provide a database session
def get_db():
    """
    Creates a database session, yields it for use,
    and closes the session to ensure proper resource management.
    """

    db = SessionLocal()  # Step 1: Create a database session object
    try:
        yield db  # Step 2: Yield the session object to the caller
    finally:
        db.close()  # Step 3: Close the session to release resources

# TODO 7: Define a dependency object for type hinting and injection
db_dependency = Annotated[Session, Depends(get_db)]
user_dendency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserVerification(BaseModel):
    password : str 
    new_password : str = Field(min_length=6)

# Endpoint to retrieve user information
@router.get("")
async def get_user_info(user: user_dendency, db : db_dependency): 
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    # Query the user by their ID
    return  db.query(Users).filter(Users.id == user.get("id")).first()

    
# Endpoint to change the user's password
@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dendency, 
    db: db_dependency,  
    user_verification: UserVerification
):
    """
    Changes the authenticated user's password.
    """
    # Check if user is authenticated
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    # Query the user by their ID
    current_user = db.query(Users).filter(Users.id == user.get("id")).first()
    
    # If user not found, raise 404 error
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Verify the current password
    if not bcrypt_context.verify(user_verification.password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error on password change")
    
    # Hash the new password and update the user record
    current_user.hashed_password = bcrypt_context.hash(user_verification.new_password)
    
    # Commit the changes to the database
    db.commit()
        
    return {"message": "Password changed successfully"}

# Endpoint to change the user's phone number
@router.put("/phoneNumber", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dendency, db: db_dependency, p_phone_number: str):
    """
    Change the phone number for a user.
    """
    
    # Check if the user is authenticated
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    # Query the database for the current user
    current_user = db.query(Users).filter(Users.id == user.get("id")).first()
    
    # If the user is not found in the database, raise an authentication error
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User Not Found")
    
    # Update the phone number for the current user
    current_user.phone_number = p_phone_number
    
    # Commit the changes to the database
    db.commit()
    
    # Return a success message
    return {"message": "Phone number changed successfully"}
