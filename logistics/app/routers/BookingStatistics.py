from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.mongodb import get_booking_statistics_collection
from app.crud.BookingStatistics import (
    create_booking_statistic,
    get_all_booking_statistics,
    get_booking_statistic_by_id,
    update_booking_statistic,
    delete_booking_statistic
)

class BookingStatisticCreate(BaseModel):
    logistic_company_id: int
    total_bookings: int
    month: str
    year: int

class BookingStatisticResponse(BaseModel):
    id: str
    logistic_company_id: int
    total_bookings: int
    month: str
    year: int

booking_router = APIRouter()

@booking_router.post("/statistics/", response_model=BookingStatisticResponse, summary="Create a new booking statistic",
    description="Adds a new booking statistic to the MongoDB collection.",)
async def create_statistic(statistic: BookingStatisticCreate):
    collection = get_booking_statistics_collection()
    stat_id = create_booking_statistic(collection, statistic.dict())
    return {**statistic.dict(), "id": stat_id}

@booking_router.get("/statistics/", response_model=List[BookingStatisticResponse], summary="Get all booking statistics",
    description="Retrieves all booking statistics from the MongoDB collection.",)
async def read_statistics():
    collection = get_booking_statistics_collection()
    return get_all_booking_statistics(collection)

@booking_router.get("/statistics/{id}", response_model=BookingStatisticResponse, summary="Get a specific booking statistic",
    description="Retrieves a specific booking statistic by its ID.",)
async def read_statistic(id: str):
    collection = get_booking_statistics_collection()
    stat = get_booking_statistic_by_id(collection, id)
    if stat:
        return stat
    raise HTTPException(status_code=404, detail="Statistic not found")

@booking_router.put("/statistics/{id}", response_model=BookingStatisticResponse, summary="Update a specific booking statistic",
    description="Updates a specific booking statistic by its ID.",)
async def update_statistic(id: str, statistic: BookingStatisticCreate):
    collection = get_booking_statistics_collection()
    if update_booking_statistic(collection, id, statistic.dict()):
        updated_stat = get_booking_statistic_by_id(collection, id)
        return updated_stat
    raise HTTPException(status_code=404, detail="Statistic not found")

@booking_router.delete("/statistics/{id}", summary="Delete a specific booking statistic",
    description="Deletes a specific booking statistic by its ID.",)
async def delete_statistic(id: str):
    collection = get_booking_statistics_collection()
    if delete_booking_statistic(collection, id):
        return {"message": "Statistic deleted successfully"}
    raise HTTPException(status_code=404, detail="Statistic not found")
