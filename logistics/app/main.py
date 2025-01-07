from fastapi import FastAPI
from app.database import engine, get_db
from app.models import Base
from app.routers import customers, agents, users ,bookings # Import routers for customers and agents
from app.crud.customers import populate_categories, populate_customer_types
# from app.crud.users import populate_permissions

from app.routers.BookingStatistics import booking_router



# Initialize FastAPI app
app = FastAPI()

# Create tables (if they don't exist already)
Base.metadata.create_all(bind=engine)

# Include routers for customers and agents
app.include_router(customers.router, prefix="/thisaiapi/customers", tags=["Customers"])
app.include_router(agents.router, prefix="/thisaiapi/agents", tags=["Agents"])
app.include_router(users.router, prefix="/thisaiapi/users", tags=["Users"])
app.include_router(bookings.router, prefix="/thisaiapi/bookings", tags=["Bookings"])


app.include_router(booking_router, prefix="/thisaiapi/bookingstatics", tags=["Booking Statistics"])


@app.on_event("startup")
async def on_startup():
    db = next(get_db())  # Get the database session
    try:
        # Populate categories and customer types only if they don't already exist
        populate_categories(db)  # Populate categories
        populate_customer_types(db)  # Populate customer types

        # populate_permissions(db)
    finally:
        db.close()  # Always close the session after use to avoid resource leaks
