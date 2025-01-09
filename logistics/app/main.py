from fastapi import FastAPI
from app.databases.mysqldb import engine, get_db
from app.models.base import Base
from app.models.users import Users
from app.models.quotations import Quotations
from app.models.addressbooks import AddressBook
from app.models.bookings import Bookings
from app.models.customers import Customer
from app.routers import customers, agents, users ,bookings
from app.crud.customers import populate_categories, populate_customer_types
from app.routers.BookingStatistics import booking_router
import logging

# Initialize FastAPI app
app = FastAPI()

# Create tables (if they don't exist already)
Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)

# Include routers for customers and agents
app.include_router(customers.router, prefix="/thisaiapi/customers", tags=["Customers"])
app.include_router(agents.router, prefix="/thisaiapi/agents", tags=["Agents"])
app.include_router(users.router, prefix="/thisaiapi/users", tags=["Users"])
app.include_router(bookings.router, prefix="/thisaiapi/bookings", tags=["Bookings"])
app.include_router(booking_router, prefix="/thisaiapi/bookingstatics", tags=["Booking Statistics"])


@app.on_event("startup")
async def on_startup():
    logging.info("App is starting...")
    db = next(get_db())  # Get the database session
    try:
        logging.info("Populating categories...")
        populate_categories(db)
        logging.info("Populating customer types...")
        populate_customer_types(db)
    except Exception as e:
        logging.error(f"Error during startup: {e}")
    finally:
        if db:
            db.close()  # Always close the session after use

