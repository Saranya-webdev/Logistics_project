from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client.test_database
print(db.list_collection_names())
