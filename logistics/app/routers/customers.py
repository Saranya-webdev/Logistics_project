from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.customers import CustomerCreate, CustomerResponse, CustomerUpdate, CustomerCategoryResponse, CustomerTypeResponse
from app.crud.customers import get_customer, create_customer, update_customer, delete_customer, get_customer_booking
from app.databases.mysqldb import get_db
from typing import List
from sqlalchemy.exc import IntegrityError
from app.models import Customer
from sqlalchemy.orm import joinedload
import logging

router = APIRouter()

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create customer
@router.post("/createcustomer/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED,
             description="Create a new customer and return the created customer object.")
async def create_customer_api(customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        return create_customer(db, customer.dict())
    except IntegrityError as e:
        logger.error(f"Integrity error while creating customer: {str(e)}")
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(status_code=400, detail="Customer with this email already exists")
        raise HTTPException(status_code=500, detail="Database error occurred")

# Search for customers by name, email, or mobile
@router.get("/getcustomer", response_model=List[CustomerResponse])
async def get_customer(search_term: str, db: Session = Depends(get_db)):
    customers = db.query(Customer).filter(
        Customer.customer_name.ilike(f"%{search_term}%") |
        Customer.email.ilike(f"%{search_term}%") |
        Customer.mobile.ilike(f"%{search_term}%")
    ).options(
        joinedload(Customer.category),
        joinedload(Customer.customer_type)
    ).all()

    if not customers:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer_responses = [
        CustomerResponse(
            customer_id=customer.customer_id,
            customer_name=customer.customer_name,
            email=customer.email,
            mobile=customer.mobile,
            company=customer.company,
            address=customer.address,
            city=customer.city,
            state=customer.state,
            pincode=customer.pincode,
            country=customer.country,
            taxid=customer.taxid,
            licensenumber=customer.licensenumber,
            designation=customer.designation,
            is_active=customer.is_active,
            category=CustomerCategoryResponse(id=customer.category.id, name=customer.category.name) if customer.category else None,
            customer_type=CustomerTypeResponse(id=customer.customer_type.id, name=customer.customer_type.name) if customer.customer_type else None
        ) for customer in customers
    ]

    return customer_responses

# Get all customers
@router.get("/allcustomers", response_model=List[CustomerResponse])
def get_all_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).options(joinedload(Customer.bookings)).all()
    return [CustomerResponse(
        customer_id=customer.customer_id,
        customer_name=customer.customer_name,
        email=customer.email,
        mobile=customer.mobile,
        company=customer.company,
        address=customer.address,
        city=customer.city,
        state=customer.state,
        pincode=customer.pincode,
        country=customer.country,
        taxid=customer.taxid,
        licensenumber=customer.licensenumber,
        designation=customer.designation,
        is_active=customer.is_active,
        category=customer.category,
        customer_type=customer.customer_type
    ) for customer in customers]

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

# Get customer with booking details
@router.get("/customer/{customer_id}/booking")
def get_customer_booking_details(customer_id: int, db: Session = Depends(get_db)):
    return get_customer_booking(customer_id, db)

# Delete customer by ID
@router.delete("/{customer_id}/deletecustomer", status_code=status.HTTP_200_OK)
async def delete_customer_api(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer(db, customer_id)  # Ensure you're getting the full model instance here, not a dictionary
    if not customer:
        logger.error(f"Customer ID {customer_id} not found")
        raise HTTPException(status_code=404, detail="Customer not found")
    delete_customer(db, customer_id)
    # You can access model attributes here directly if customer is an instance of the model
    return {"detail": f"Customer {customer.customer_name} (ID: {customer.customer_id}) deleted successfully"}

