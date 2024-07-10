# Tutorial on Using Alembic with FastAPI 🚀

## What is Alembic? 🤔

Alembic is a lightweight database migration tool for usage with SQLAlchemy, a SQL toolkit and Object-Relational Mapping (ORM) library for Python. It helps you manage database schema changes over time.

### Prerequisites 📋

1. Basic understanding of Python and FastAPI.
2. Installed Python environment (Python 3.7+).
3. Installed FastAPI and SQLAlchemy.
4. Installed a database system (e.g., PostgreSQL, MySQL, SQLite).

### Step-by-Step Tutorial 🛠️

#### 1. Set Up FastAPI Project 🗂️

1. **Create a project directory**:

   ```bash
   mkdir fastapi_alembic_example
   cd fastapi_alembic_example
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install FastAPI, Uvicorn, SQLAlchemy, and Alembic**:

   ```bash
   pip install fastapi uvicorn sqlalchemy alembic
   ```

4. **Create a basic FastAPI application**:

   ```python
   # main.py
   from fastapi import FastAPI
   from sqlalchemy import create_engine, Column, Integer, String
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.orm import sessionmaker

   app = FastAPI()

   DATABASE_URL = "sqlite:///./test.db"
   engine = create_engine(DATABASE_URL)
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   Base = declarative_base()

   class User(Base):
       __tablename__ = "users"
       id = Column(Integer, primary_key=True, index=True)
       name = Column(String, index=True)
       email = Column(String, unique=True, index=True)

   Base.metadata.create_all(bind=engine)

   @app.get("/")
   def read_root():
       return {"Hello": "World"}
   ```

#### 2. Set Up Alembic ⚙️

1. **Initialize Alembic**:

   ```bash
   alembic init alembic
   ```

2. **Configure Alembic**:

   - Open `alembic.ini` and set the `sqlalchemy.url` to your database URL:

     ```ini
     sqlalchemy.url = sqlite:///./test.db
     ```

   - Update `alembic/env.py` to include your SQLAlchemy models:

     ```python
     from logging.config import fileConfig

     from sqlalchemy import engine_from_config
     from sqlalchemy import pool

     from alembic import context

     # this is the Alembic Config object, which provides
     # access to the values within the .ini file in use.
     config = context.config

     # Interpret the config file for Python logging.
     # This line sets up loggers basically.
     fileConfig(config.config_file_name)

     # add your model's MetaData object here
     # for 'autogenerate' support
     # from myapp import mymodel
     # target_metadata = mymodel.Base.metadata
     from main import Base  # Import your Base object
     target_metadata = Base.metadata

     # other values from the config, defined by the needs of env.py,
     # can be acquired:
     # my_important_option = config.get_main_option("my_important_option")
     # ... etc.


     def run_migrations_offline():
         """Run migrations in 'offline' mode.
         This configures the context with just a URL
         and not an Engine, though an Engine is also acceptable
         here. By skipping the Engine creation we don't even need a
         DBAPI to be available.
         Calls to context.execute() here emit the given string to the
         script output.
         """
         url = config.get_main_option("sqlalchemy.url")
         context.configure(
             url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
         )

         with context.begin_transaction():
             context.run_migrations()


     def run_migrations_online():
         """Run migrations in 'online' mode.
         In this scenario we need to create an Engine
         and associate a connection with the context.
         """
         connectable = engine_from_config(
             config.get_section(config.config_ini_section),
             prefix="sqlalchemy.",
             poolclass=pool.NullPool,
         )

         with connectable.connect() as connection:
             context.configure(connection=connection, target_metadata=target_metadata)

             with context.begin_transaction():
                 context.run_migrations()


     if context.is_offline_mode():
         run_migrations_offline()
     else:
         run_migrations_online()
     ```

#### 3. Creating and Applying Migrations 📝

1. **Create a new migration**:

   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

2. **Apply the migration**:

   ```bash
   alembic upgrade head
   ```

#### 4. Using Alembic with FastAPI 🔄

1. **Add new models**:

   ```python
   # main.py
   class Item(Base):
       __tablename__ = "items"
       id = Column(Integer, primary_key=True, index=True)
       title = Column(String, index=True)
       description = Column(String, index=True)
   ```

2. **Generate and apply new migrations**:

   ```bash
   alembic revision --autogenerate -m "Add Item model"
   alembic upgrade head
   ```

3. **Run the FastAPI application**:
   ```bash
   uvicorn main:app --reload
   ```

#### 5. Full Directory Structure 📂

Your project should now have the following structure:

```
fastapi_alembic_example/
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── alembic.ini
├── main.py
├── test.db
└── env/
    ├── bin/
    ├── include/
    ├── lib/
    └── pyvenv.cfg
```

### Conclusion 🎉

You have now set up a FastAPI application using Alembic for database migrations. With Alembic, you can manage and evolve your database schema efficiently. You can continue to develop your application and easily apply changes to the database structure as needed.

### Common Alembic Commands 🛠️

Here's a table of common Alembic commands you will frequently use:

| Command                                          | Description                                               |
| ------------------------------------------------ | --------------------------------------------------------- |
| `alembic init <directory>`                       | Initialize a new Alembic environment.                     |
| `alembic revision --autogenerate -m "<message>"` | Create a new migration script with autogenerated changes. |
| `alembic upgrade <revision>`                     | Apply the migrations up to the specified revision.        |
| `alembic downgrade <revision>`                   | Revert migrations back to the specified revision.         |
| `alembic current`                                | Display the current revision of the database.             |
| `alembic history`                                | List all migrations and their status.                     |
| `alembic heads`                                  | Show the current heads in the script directory.           |
| `alembic branches`                               | Show the branch points.                                   |
| `alembic show <revision>`                        | Show the details of a particular revision.                |
| `alembic edit <revision>`                        | Edit a particular revision.                               |
| `alembic merge <revisions>`                      | Merge two or more revisions together.                     |
