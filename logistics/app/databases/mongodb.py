from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from dotenv import load_dotenv

#load enviroment variables
load_dotenv()


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Access the environment variables
MONGO_DETAILS = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
collection_name = os.getenv("COLLECTION_NAME", "logistics_mongodb")

try:
    client = AsyncIOMotorClient(MONGO_DETAILS)
    database = client[collection_name]
    logger.info("Successfully connected to the MongoDB.")
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {str(e)}")
    database = None


# Collections
quotations_collection = database["quotations"]
bookings_stats_collection = database["booking_statistics"]

def get_booking_statistics_collection():
    return bookings_stats_collection


# def get_user_by_email(email):
#     """
#     Fetch a user from the 'quotations' collection based on the provided email.
#     The email is stored in the 'user.user_email' field.

#     :param email: str - The email of the user to search for.
#     :return: dict - The quotation document if found, else None.
#     """
#     try:
#         # Search for a quotation document where the user.email matches the provided email
#         quotation = quotations_collection.find_one({"user.user_email": email})
#         return quotation
#     except Exception as e:
#         print(f"Error fetching user by email: {e}")
#         return None