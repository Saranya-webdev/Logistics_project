# app/main.py
"""
main.py - Entry point for the FastAPI application.

This module initializes the FastAPI app, sets up the database, includes routers, 
and configures logging.
"""

from fastapi import FastAPI
from app.databases.mysqldb import engine, get_db
from app.models.base import Base
from app.routers import customers, agents, bookings, quotations, addressbook, carriers, thisaiprofiles
from app.crud.customers import populate_categories, populate_customer_types
from app.routers.BookingStatistics import booking_router
import logging
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables (if they don't exist already) during startup
Base.metadata.create_all(bind=engine)

# Configure logging to display informational messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Include routers for different modules
app.include_router(customers.router, prefix="/thisaiapi/customers", tags=["Customers"], description="Operations related to customers")
app.include_router(agents.router, prefix="/thisaiapi/agents", tags=["Agents"], description="Operations related to agents")
app.include_router(thisaiprofiles.router, prefix="/thisaiapi/associates", tags=["Associates"], description="Operations related to associates")
app.include_router(carriers.router, prefix="/thisaiapi/carriers", tags=["Carriers"], description="Operations related to carrier")
app.include_router(bookings.router, prefix="/thisaiapi/bookings", tags=["Bookings"], description="Operations related to bookings")
app.include_router(quotations.router, prefix='/thisaiapi/quotations', tags=["Quotations"], description="Operations related to quotations")
app.include_router(addressbook.router, prefix='/thisaiapi/addressbook', tags=["AddressBook"], description="Operations related to address-books")
app.include_router(booking_router, prefix="/thisaiapi/bookingstatics", tags=["Booking Statistics"], description="Operations related to booking-statics")

# Startup event
@app.on_event("startup")
async def on_startup():
    """
    This event is triggered when the application starts. It logs the start 
    of the application, populates categories and customer types, and handles 
    database session management.
    """
    logger.info("App is starting...")
    
    db = next(get_db())  # Get the database session
    try:
        # Populate initial data
        logger.info("Populating categories...")
        populate_categories(db)
        logger.info("Populating customer types...")
        populate_customer_types(db)
    except Exception as e:
        logger.error(f"Error during startup: {e}")
    finally:
        if db:
            db.close()  # Ensure the database session is closed after use
            logger.info("Database session closed.")
