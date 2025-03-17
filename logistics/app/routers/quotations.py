from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session,joinedload
from app.schemas.quotations import QuotationResponse, QuotationDetailedResponse, QuotationUpdate,ShippingRateRequest,QuotationDetailedResponse,QuotationCreate
from app.schemas.bookings import ShippingRateRequest, ShippingRateResponse
from app.databases.mysqldb import get_db
from app.databases.mongodb import get_mongo_db
from typing import List
from sqlalchemy.exc import IntegrityError
from app.models.quotations import Quotations
from fastapi.exceptions import RequestValidationError
# from app.crud.quotations import get_quotation, update_quotation, delete_quotation
from app.service.quotations import update_quotation_service,create_quotation_service,get_all_quotations_service, fetch_shipping_rates,get_single_quotation_service
from pydantic import ValidationError
import logging
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from motor.motor_asyncio import AsyncIOMotorDatabase

logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/createquotation/", response_model=QuotationResponse, status_code=status.HTTP_201_CREATED)
async def create_quotation_api(quotation: QuotationCreate, db=Depends(get_mongo_db)):  # Use get_mongo_db

    try:
        quotation_data = quotation.dict()
        created_quotation = await create_quotation_service(db, quotation_data)
        return created_quotation

    except DuplicateKeyError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quotation with this identifier already exists")

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {str(e)}")

    
# GET quotation by ID
@router.get("/{quotation_id}/viewquotation/", response_model=QuotationResponse)
async def get_single_quotation(quotation_id: str, db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    try:
        quotation = await get_single_quotation_service(quotation_id, db)
        if not quotation:
            raise HTTPException(status_code=404, detail="Quotation not found")
        return quotation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# GET all quotations
@router.get("/allquotations/", response_model=List[QuotationResponse])
async def get_quotations_api(db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    try:
        quotations = await get_all_quotations_service(db)
        return quotations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving quotations: {str(e)}")


@router.put("/{quotation_id}/updatequotation")
async def update_quotation_api(quotation: ShippingRateRequest, quotation_id: str, db = Depends(get_mongo_db)):
    try:
        # Log received data
        logging.info(f"Received quotation data for update: {quotation.dict()}")
        logging.info(f"Received quotation_id: {quotation_id}")

        # Call the service layer to process the update
        updated_quotation = await update_quotation_service(db, quotation_id, quotation.dict())
        logging.info(f"Updated quotation response: {updated_quotation}")

        return updated_quotation  # Return the result from the service layer

    except Exception as e:
        logging.error(f"Error in updating quotation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in updating quotation: {str(e)}")





# DELETE quotation by ID
# @router.delete("/{quotation_id}/deletequotation", status_code=status.HTTP_200_OK)
# async def delete_quotation_api(quotation_id: int, db: Session = Depends(get_db)):
#     db_quotation = get_quotation(db, quotation_id)
#     if not db_quotation:
#         raise HTTPException(status_code=404, detail="Quotation not found")
#     delete_quotation(db, quotation_id)
#     return {"detail": f"Quotation (ID: {quotation_id}) deleted successfully"}

