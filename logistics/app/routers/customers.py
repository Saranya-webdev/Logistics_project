from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.customers import CustomerCreate, CustomerResponse, CustomerUpdate, CustomerListResponse, CustomerDetailResponse, CustomerBookingListResponse
from app.schemas.bookings import BookingDetailedResponse
from app.crud.customers import get_customer, create_customer, update_customer, delete_customer, get_customer_booking_details,get_all_customers,get_customer_booking_list
from app.databases.mysqldb import get_db
from typing import List
from sqlalchemy.exc import IntegrityError
import logging
from app.models.bookings import Bookings

router = APIRouter() # used to define a group of related API routes.

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create customer
@router.post("/createcustomer/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer_api(customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        return create_customer(db, customer.dict())
    except IntegrityError as e:
        logger.error(f"Integrity error while creating customer: {str(e)}")
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(status_code=400, detail="Customer with this email already exists")
        raise HTTPException(status_code=500, detail="Database error occurred")

# Search for customers by name, email, or mobile
@router.get("/getcustomer", response_model=List[CustomerDetailResponse])
async def get_customer_api(search_term: str, db: Session = Depends(get_db)):
    customers = get_customer(db, search_term)
    if isinstance(customers, dict) and "detail" in customers:
        if customers["detail"] == "Customer not found":
            raise HTTPException(status_code=404, detail=customers["detail"])
        elif customers["detail"] == "Search term cannot be empty":
            raise HTTPException(status_code=400, detail=customers["detail"])
    return customers


# Get all customers (name, mobile, email)
@router.get("/allcustomers", response_model=List[CustomerListResponse])
def get_all_customers_api(db: Session = Depends(get_db)):
    customers = get_all_customers(db)  # Modify this function to fetch only name, mobile, and email
    return customers

# Get customer with booking list
@router.get("/customer/{customer_id}/bookinglist", response_model=CustomerBookingListResponse)
def get_customer_booking_list_api(customer_id: int, db: Session = Depends(get_db)):
    customer_bookings = get_customer_booking_list(customer_id, db)  # This now returns a dictionary
    return CustomerBookingListResponse(
        customer_name=customer_bookings['customer_name'],
        bookings=customer_bookings['bookings']
    )


# Get customer booking details
@router.get("/customer/{customer_id}/booking/{booking_id}", response_model=BookingDetailedResponse)
async def get_customer_booking(customer_id: int, booking_id: int, db: Session = Depends(get_db)):
    # Replace with your actual logic to fetch booking details
    booking = db.query(Bookings).filter(Bookings.customer_id == customer_id, Bookings.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

# Update customer by ID
@router.put("/{customer_id}/updatecustomer", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
async def edit_customer_api(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    if not any(value is not None for value in customer.dict().values()):
        raise HTTPException(status_code=400, detail="No fields to update")
    existing_customer = get_customer(db, customer_id)
    if existing_customer is None:
        raise HTTPException(status_code=404, detail="Customer ID not found")
    updated_customer = update_customer(db, customer_id, customer.dict(exclude_unset=True))
    return updated_customer


# Delete customer by ID
@router.delete("/{customer_id}/deletecustomer", status_code=status.HTTP_200_OK)
async def delete_customer_api(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer(db, customer_id)
    if not customer:
        logger.error(f"Customer ID {customer_id} not found")
        raise HTTPException(status_code=404, detail="Customer not found")
    delete_customer(db, customer_id)
    return {"detail": f"Customer {customer.customer_name} (ID: {customer.customer_id}) deleted successfully"}