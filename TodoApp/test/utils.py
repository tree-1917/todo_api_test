from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from ..models import Todos,Users
from fastapi.testclient import TestClient as tc
import pytest 
from ..routers.auth import bcrypt_context

# TODO: Define the test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"  # Test database

# TODO: Create the test engine with StaticPool for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# TODO: Create testing session local
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# TODO: Create all tables for the test database
Base.metadata.create_all(bind=engine)

# TODO: Override the get_db dependency to use the test database session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# TODO: Override the get_current_user dependency to return a test user
def override_get_current_user():
    return {'username': "Hassan", "id": 1, "user_role": "admin"}

# TODO: Create a test client for the FastAPI app
client = tc(app)

# TODO: Define a pytest fixture to set up a test todo item
@pytest.fixture
def test_todo():
    # TODO: Create a new Todos object
    todo = Todos(
        title="learn to code",
        description="need to learn everyday!",
        priority=3,
        complete=False,
        owner_id=1,
    )
    db = TestingSessionLocal()
    # TODO: Add the todo item to the database and commit
    db.add(todo)
    db.commit()
    # TODO: Yield the todo item for use in tests
    yield todo
    # TODO: Clean up the database after the test
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


# 
@pytest.fixture 
def test_user() : 
    user = Users(
        username = "Hassan",
        email = "Hassan@xyz.com",
        first_name = "Hassan",
        last_name = "Ali",
        hashed_password = bcrypt_context.hash("123"),
        role="admin", 
        phone_number = "(111)111-1111" 
    )
    db = TestingSessionLocal() 
    db.add(user)
    db.commit() 
    yield user 
    with engine.connect() as connection : 
        connection.execute(text("DELETE FROM users;"))
        connection.commit() 
        