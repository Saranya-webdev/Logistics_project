from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
MONGO_DB_NAME = "logistics_mongodb" 

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB_NAME]

bookings_stats_collection = mongo_db["booking_statistics"]

def get_booking_statistics_collection():
    return bookings_stats_collection
