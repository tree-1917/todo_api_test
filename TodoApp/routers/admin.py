# == Import necessary libraries ==
# TODO 1: Import necessary libraries from typing and Pydantic
from typing import Annotated
from pydantic import BaseModel, Field
# TODO 2: Import necessary modules from SQLAlchemy and FastAPI
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, status
# TODO 3: Import the Todos model
from ..models import Todos
# TODO 4: Import database connection details (engine and session factory)
from ..database import SessionLocal

from .auth import get_current_user 

# TODO 5: Create an instance of APIRouter with prefix and tags
router = APIRouter(
    prefix="/admin",
    tags=["admin"]
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


# Endpoint to retrieve all Todo items
@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dendency, db: db_dependency):
    """
    Retrieves all Todo items from the database if the user is authenticated as an admin.
    If authentication fails, raises HTTP 401 Unauthorized error.
    """
    # Check if the user is authenticated and has admin role
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    # Return all Todo items
    return db.query(Todos).all()



# Endpoint to delete a specific Todo item by its ID
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(user: user_dendency, db: db_dependency, todo_id: int):
    # [1] Validation
    if user is None or user.get("user_role") != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    # [2] Delete Todo
    todo_item = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not Found")

    db.delete(todo_item)
    db.commit()
    
    return {"Message": "Delete Item Successfully"}
