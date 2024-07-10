# === Import necessary libraries ===
from .database import Base  # Import the Base class from your database.py file
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey  # Import column types from SQLAlchemy

# === Define the Todos model ===

# User model
class Users(Base):
    __tablename__ = 'users'  # Name of the table in the database
    
    # Column for the primary key, which is an auto-incrementing integer
    id = Column(Integer, primary_key=True, index=True)
    
    # Column for the email of the user, which must be unique
    email = Column(String, unique=True)
    
    # Column for the username of the user, which is a string
    username = Column(String)
    
    # Column for the first name of the user, which is a string
    first_name = Column(String)
    
    # Column for the last name of the user, which is a string
    last_name = Column(String)
    
    # Column for the hashed password of the user, which is a string
    hashed_password = Column(String)
    
    # Column to indicate if the user is active or not, which is a boolean with a default value of True
    is_active = Column(Boolean, default=True)
    
    # Column for the role of the user, which is a string
    role = Column(String)

    # # Column for the phone number of the user, which is a string 
    phone_number = Column(String)
    
# Todos model
class Todos(Base):
    __tablename__ = "todos"  # Name of the table in the database
    
    # Column for the primary key, which is an auto-incrementing integer
    id = Column(Integer, primary_key=True, index=True)
    
    # Column for the title of the todo, which is a string
    title = Column(String)
    
    # Column for the description of the todo, which is a string
    description = Column(String)
    
    # Column for the priority of the todo, which is an integer
    priority = Column(Integer)
    
    # Column to indicate if the todo is complete or not, which is a boolean with a default value of False
    complete = Column(Boolean, default=False)
    
    # Column to establish a foreign key relationship with the Users table
    owner_id = Column(Integer, ForeignKey("users.id"))
