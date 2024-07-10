# == Import necessary libraries ==
from fastapi import  FastAPI
from .routers import auth,todos,admin,user
# Import database models
from .models import Base
# Import database connection details (engine and session factory)
from .database import engine
from starlette import staticfiles
# Create the FastAPI application
app = FastAPI()

# Create the database tables (if they don't exist)
Base.metadata.create_all(bind=engine)

# mount static 
# app.mount("/static", staticfiles(directory="static"), name='static')

# Root 
@app.get("/")
async def root(): 
    return {"Message" : "Welcome to Todo App V0.0"}

# include router 
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)

