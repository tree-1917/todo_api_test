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
    prefix="/todo",
    tags=["todo"]
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

# TODO 8: Create a Pydantic Request model to handle new Todos
class TodoRequest(BaseModel):
    title: str = Field(min=3)  # Define the title field with a minimum length of 3
    description: str = Field(min=3, max=100)  # Define the description field with a minimum length of 3 and maximum of 100
    priority: int = Field(gt=0, lt=6)  # Define the priority field with a range of 1-5
    complete: bool  # Define the complete field as a boolean

# TODO 9: Define a GET endpoint to fetch all todos
@router.get("", status_code=status.HTTP_200_OK)
async def read_all_todo(user: user_dendency,db: db_dependency):
    """
    This endpoint retrieves all todos from the database.
    """
    if user is None : 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    # TODO 9.1: Query the database to get all todos
    todo_models = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()

    # TODO 9.2: Check if todos exist
    if todo_models is not None:
        # Step 1: Return the list of todos if they are found
        return todo_models

    # TODO 9.3: Raise an HTTP 404 error if no todos are found
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todos not found")

# TODO 10: Define a GET endpoint to fetch a todo by ID
@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_id(user: user_dendency ,db: db_dependency, todo_id: int = Path(gt=0)):
    """
    Retrieves a specific Todo item by its ID.

    Args:
        db (Annotated[Session, Depends(get_db)]): Injected database session.
        todo_id (int, optional): ID of the Todo item to retrieve (from path parameter).
            Must be a positive integer greater than zero. Defaults to None.
    """
    if user is None : 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Athuentication Failed")
    
    # TODO 10.1: Query the database to get the todo by ID
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
    

    # TODO 10.2: Check if the todo exists
    if todo_model is not None:
        # Step 1: Return the todo if it is found
        return todo_model

    # TODO 10.3: Raise an HTTP 404 error if the todo is not found
    raise HTTPException(status_code=404, detail="Todo not found.")

# TODO 11: Define a POST endpoint to create a new Todo item
@router.post("", status_code=status.HTTP_201_CREATED)
async def create_todo(user : user_dendency ,db: db_dependency, todo_item: TodoRequest):
    """
    Creates a new Todo item in the database.

    Args:
        db (Annotated[Session, Depends(get_db)]): Injected database session.
        todo_item (TodoRequest): Incoming Todo data to be created.

    Returns:
        dict: A dictionary containing a success message upon successful creation.
             OR raises an exception if an error occurs during database interaction.
    """

    if user is None : 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    # TODO 11.1: Create a new todo model instance with the provided todo input
    todo_model = Todos(**todo_item.model_dump(), owner_id = user.get("id"))
    
    # TODO 11.2: Add the new todo to the database session
    db.add(todo_model)
    # TODO 11.3: Commit the transaction to save the new todo in the database
    db.commit()  # Consider adding error handling here

    # TODO 11.4: Return a success message
    return {"Message": "Added New Todo Item Successfully"}

# TODO 12: Define a PUT endpoint to update an existing Todo item
@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dendency ,db: db_dependency, todo_req: TodoRequest, todo_id: int = Path(gt=0)):
    """
    Updates an existing Todo item in the database.

    Args:
        db (Annotated[Session, Depends(get_db)]): Injected database session.
        todo_id (int): ID of the Todo item to update.
        todo_req (TodoRequest): Incoming data containing updates for the Todo item.

    Returns:
        None: No content is returned in the body on successful update.
             OR raises an HTTPException if the Todo is not found.
    """
    if user is None : 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    
    # TODO 12.1: Query the database to get the todo by ID
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get("id")).first()
    # TODO 12.2: Check if the todo exists
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")

    # TODO 12.3: Update the todo attributes with the provided data
    todo_model.title = todo_req.title
    todo_model.description = todo_req.description
    todo_model.priority = todo_req.priority
    todo_model.complete = todo_req.complete

    # TODO 12.4: Add the updated todo model to the session
    db.add(todo_model)  # Not strictly necessary in this case
    # TODO 12.5: Commit the transaction to save the updated todo in the database
    db.commit()

    # TODO 12.6: Return a success message
    return {"Message": "Updated Todo Successfully"}

# TODO 13: Define a DELETE endpoint to delete a Todo item
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dendency , db: db_dependency, todo_id: int = Path(gt=0)):
    """
    Deletes an existing Todo item from the database.

    Args:
        db (Annotated[Session, Depends(get_db)]): Injected database session.
        todo_id (int): ID of the Todo item to delete.

    Returns:
        dict: A dictionary containing a success message upon successful deletion.
             OR raises an HTTPException if the Todo is not found.
    """
    if user is None : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")

    # TODO 13.1: Query the database to get the todo by ID
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    # TODO 13.2: Check if the todo exists
    if todo_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")

    # TODO 13.3: Delete the todo from the database
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    # TODO 13.4: Commit the transaction to save the changes in the database
    db.commit()

    # TODO 13.5: Return a success message
    return {"Message": "Successfully Deleted Todo item"}
