# == Import necessary libraries ==
# TODO 1: Import necessary libraries
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status  # Import necessary modules from FastAPI
from pydantic import BaseModel  # Import BaseModel from Pydantic for data validation
from ..models import Users  # Import the Users model
from passlib.context import CryptContext
from ..database import SessionLocal 
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

# TODO 2: Create an instance of APIRouter
router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

# Jwt 
# TODO 3: Define JWT settings
SECRET_KEY = "e5a6dbbdaeb1bcf184223e137bce2795f35ab1ed5b86f7a6a1d44457e2078a11"
ALG = "HS256"

# TODO 4: Initialize the CryptContext for password hashing using bcrypt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

# TODO 5: Define Pydantic models for user input and token
class UserIn(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number : str

class Token(BaseModel):
    access_token: str
    token_type: str

# TODO 6: Define dependency function to provide database session
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

# Dependency object for type hinting and injection
db_dependency = Annotated[Session, Depends(get_db)]

# TODO 3.5: Helper Method to find the User
def _auth_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()  # Step 1: Query the user by username

    # Step 2: Check if user exists and password is correct
    if not user: 
        return False 
    if not bcrypt_context.verify(password, user.hashed_password): 
        return False 

    return user  # Step 3: Return the user if authentication is successful

# TODO 3.5: Helper Method to Create an Access token
def _create_access_token(username: str, user_id: int,role : str,  expires_delta: timedelta):
    # Step 1: Initialize the payload with user details
    encode = {"username": username, "id": user_id, 'role' : role}
    
    # Step 2: Calculate the expiration time for the token
    expiers = datetime.utcnow() + expires_delta
    
    # Step 3: Update the payload with the expiration time
    encode.update({"exp": expiers})
    
    # Step 4: Encode the payload into a JWT using the secret key and algorithm
    return jwt.encode(encode, SECRET_KEY, algorithm=ALG)

# find current User 
async def get_current_user(token : Annotated[str, Depends(oauth2_bearer)]): 
    try : 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALG])
        username : str = payload.get('username')
        user_id : int = payload.get("id")
        user_role : str = payload.get('role')
        
        if username is None or user_id is None : 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {"username" : username , "id" : user_id , "user_role" : user_role}
    except JWTError : 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")

# TODO 7: Define a POST endpoint to create a new user
@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, UserReq: UserIn):
    # Step 1: Check if the email already exists in the database
    if db.query(Users).filter(Users.email == UserReq.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
   
    # Step 2: Create a new user model instance with the provided user input
    user_model = Users(
        email=UserReq.email,
        username=UserReq.username,
        first_name=UserReq.first_name,
        last_name=UserReq.last_name,
        role=UserReq.role,
        hashed_password=bcrypt_context.hash(UserReq.password),
        is_active=True,
        phone_number=UserReq.phone_number
    )
    # Step 3: Save the new user to the database
    db.add(user_model)
    db.commit()
        
    # Step 4: Return a success message
    return {"Message": "Added User Successfully"}

# TODO 8: Define a POST endpoint to handle user login and generate access tokens
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    # Step 1: Authenticate the user using the provided username and password
    user = _auth_user(form_data.username, form_data.password, db)
    
    # Step 2: If authentication fails, raise an HTTP 404 error with a relevant message
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password is incorrect.")
    
    # Step 3: Create an access token for the authenticated user
    token = _create_access_token(user.username, user.id, user.role,timedelta(minutes=20))
    
    # Step 4: Return the access token and token type
    return {'access_token': token, 'token_type': 'bearer'}
