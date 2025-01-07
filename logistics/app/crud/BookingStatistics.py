from pymongo.collection import Collection
from bson import ObjectId
from typing import Optional

def create_booking_statistic(collection: Collection, statistic_data: dict) -> str:
    result = collection.insert_one(statistic_data)
    return str(result.inserted_id)

def get_all_booking_statistics(collection: Collection) -> list:
    return [{**stat, "id": str(stat["_id"])} for stat in collection.find()]

def get_booking_statistic_by_id(collection: Collection, stat_id: str) -> Optional[dict]:
    stat = collection.find_one({"_id": ObjectId(stat_id)})
    return {**stat, "id": str(stat["_id"])} if stat else None

def update_booking_statistic(collection: Collection, stat_id: str, update_data: dict) -> bool:
    result = collection.update_one({"_id": ObjectId(stat_id)}, {"$set": update_data})
    return result.modified_count > 0

def delete_booking_statistic(collection: Collection, stat_id: str) -> bool:
    result = collection.delete_one({"_id": ObjectId(stat_id)})
    return result.deleted_count > 0
