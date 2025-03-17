from motor.motor_asyncio import AsyncIOMotorClient,AsyncIOMotorDatabase
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB Client
MONGO_DETAILS = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
collection_name = os.getenv("COLLECTION_NAME", "logistics_mongodb")
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client[collection_name]  # MongoDB client

# MongoDB Collections
quotations_collection = database["quotations"]
bookings_stats_collection = database["booking_statistics"]
create_quotations_collection = database["create_quotations"]

def get_mongo_db()-> AsyncIOMotorDatabase:
    return database  # Return MongoDB database client

def get_booking_statistics_collection():
    return bookings_stats_collection