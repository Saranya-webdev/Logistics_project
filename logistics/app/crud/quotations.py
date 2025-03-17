from sqlalchemy.orm import Session,joinedload
from app.schemas.quotations import  ShippingRateRequest
from fastapi import HTTPException
import logging
from app.models.quotations import QuotationItems,Quotations
from app.databases.mongodb import quotations_collection
from bson import ObjectId
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorDatabase


# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def create_quotation_crud(db, quotation_data):
    try:
       
        collection = db["quotations"]  
        result = await collection.insert_one(quotation_data)
        return result
    except Exception as e:
        raise Exception(f"Database error in create_quotation_crud: {str(e)}")



async def update_quotation_crud(db, filter_criteria, quotation_data):
    try:
        result = await db["quotations"].update_one(
            filter_criteria, 
            {"$set": quotation_data}, 
            upsert=False 
        )
        return result
    except Exception as e:
        raise Exception(f"Database error in update_quotation_crud: {str(e)}")


async def get_single_quotation_crud(quotation_id: str, db: AsyncIOMotorDatabase):
    try:
        if not ObjectId.is_valid(quotation_id):
            return None 
        print(f"Looking for quotation: {quotation_id}")


        quotation = await db.quotations.find_one({"_id": ObjectId(quotation_id), "status": "Saved"})
        return quotation
    except Exception as e:
        raise Exception(f"Database error in get_single_quotation_crud: {str(e)}")


async def get_all_quotations_crud(db: AsyncIOMotorDatabase):
    try:
       
        quotations_cursor = db.quotations.find({"status": "Saved"})
        quotations = await quotations_cursor.to_list(length=None)
        return quotations

    except Exception as e:
        raise Exception(f"Database error in get_all_quotations_crud: {str(e)}")


