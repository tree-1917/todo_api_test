# == Import necessary libraries ==
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 0 = Define the database URL
# SQLite database URL in this case, change as per your database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"

# 1 = Create the engine
# The engine is responsible for managing the connection to the database
# `check_same_thread=False` is specific to SQLite and allows multiple threads to interact with the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 2 = Create a session maker
# The session maker is a factory for creating new Session objects, which are used to interact with the database
# `autocommit=False` means that changes will not be automatically committed
# `autoflush=False` means that changes will not be automatically flushed to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3 = Create the base class for the declarative model
# The Base class is used to create the database models (tables)
Base = declarative_base() 