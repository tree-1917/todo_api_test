# 🚀 FastAPI Tutorial: Implementing JWT Authentication

JSON Web Tokens (JWT) are a popular way to handle authentication in modern web applications. In this tutorial, we'll walk through how to implement JWT authentication in a FastAPI application.

## 1. Setting Up the Environment 🛠️

First, make sure you have FastAPI and the necessary dependencies installed:

```bash
pip install fastapi uvicorn python-jose passlib[bcrypt] python-dotenv
```

## 2. Project Structure 🗂️

Organize your project as follows:

```text
.
├── main.py
├── auth
│   ├── __init__.py
│   ├── auth.py
│   ├── models.py
│   ├── schemas.py
│   └── utils.py
└── .env
```

## 3. Configuring Environment Variables 🔐

Create a `.env` file to store sensitive information such as the secret key:

```text
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 4. Defining Models and Schemas 📋

In `auth/models.py`, define your user model (for simplicity, we'll use an in-memory user list):

```python
from pydantic import BaseModel

class UserInDB(BaseModel):
    username: str
    hashed_password: str
```

In `auth/schemas.py`, define the schemas for your API requests and responses:

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserCreate(BaseModel):
    username: str
    password: str
```

## 5. Utility Functions 🔧

In `auth/utils.py`, add utility functions for password hashing and token creation:

```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

## 6. Authentication Logic 🔐

In `auth/auth.py`, implement the authentication logic:

```python
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from .models import UserInDB
from .schemas import Token, TokenData, User, UserCreate
from .utils import verify_password, get_password_hash, create_access_token

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In-memory user storage
fake_users_db = {
    "johndoe": UserInDB(**{"username": "johndoe", "hashed_password": get_password_hash("secret")})
}

def authenticate_user(fake_db, username: str, password: str):
    user = fake_db.get(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = fake_users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

## 7. Main Application Entry Point 🚪

In `main.py`, include the authentication router:

```python
from fastapi import FastAPI
from auth.auth import app as auth_app

app = FastAPI()

app.mount("/auth", auth_app)
```

## 8. Testing Your JWT Authentication ✅

To test your application:

1. Run your FastAPI app:

   ```bash
   uvicorn main:app --reload
   ```

2. Use a tool like Postman to send a POST request to `/auth/token` with form data:
   - `username`: `johndoe`
   - `password`: `secret`
3. Use the returned access token to access the protected `/auth/users/me/` endpoint by setting the `Authorization` header to `Bearer <access_token>`.

### Security Considerations 🔒

1. **Secret Key Management:**

   - Store your secret key in environment variables or a secrets management service.
   - Rotate your secret key regularly and ensure it is of sufficient length and randomness.

2. **Token Expiration:**

   - Set appropriate token expiration times to balance security and user convenience.
   - Implement refresh tokens if needed.

3. **HTTPS:**

   - Always use HTTPS to protect data in transit, especially when dealing with sensitive information like tokens and passwords.

4. **User Management:**
   - Implement proper user creation, password reset, and account lockout mechanisms.
   - Store passwords securely using strong hashing algorithms.

By following these steps and considerations, you can implement JWT authentication in your FastAPI application like a pro. 🚀
