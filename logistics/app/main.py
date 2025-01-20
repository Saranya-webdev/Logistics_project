# app/main.py
from fastapi import FastAPI
from app.databases.mysqldb import engine, get_db
from app.models.base import Base
from app.routers import customers, agents, users, bookings,quotations,addressbook
from app.crud.customers import populate_categories, populate_customer_types
from app.routers.BookingStatistics import booking_router
import logging

# Initialize FastAPI app
app = FastAPI()

# Create tables (if they don't exist already)
Base.metadata.create_all(bind=engine)

# Configures logging to display informational messages.
logging.basicConfig(level=logging.INFO)

# Include routers
app.include_router(customers.router, prefix="/thisaiapi/customers", tags=["Customers"])
app.include_router(agents.router, prefix="/thisaiapi/agents", tags=["Agents"])
app.include_router(users.router, prefix="/thisaiapi/users", tags=["Users"])
app.include_router(bookings.router, prefix="/thisaiapi/bookings", tags=["Bookings"])
app.include_router(quotations.router, prefix='/thisaiapi/quotations', tags=["Quotations"])
app.include_router(addressbook.router, prefix='/thisaiapi/addressbook', tags=["AddressBook"])
app.include_router(booking_router, prefix="/thisaiapi/bookingstatics", tags=["Booking Statistics"])


# Startup Event
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
