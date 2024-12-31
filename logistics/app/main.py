from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import customers, agents  # Ensuring the routers are imported correctly

# Initialize FastAPI app
app = FastAPI()

# Create tables (if they don't exist already)
Base.metadata.create_all(bind=engine)

# Include routers for customers and agents
app.include_router(customers.router, prefix="/thisaiapi/customers", tags=["Customers"])
app.include_router(agents.router, prefix="/thisaiapi/agents", tags=["Agents"])
