from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.customers import CustomerCreate, CustomerResponse, CustomerUpdate
from app.crud.customers import get_customer, create_customer, update_customer, delete_customer
from app.databases.mysqldb import get_db
from typing import List
from sqlalchemy.exc import IntegrityError
from app.models import Customer, Bookings, Quotations
from sqlalchemy.orm import joinedload
from app.service.customers import create_customer, update_customer
import logging

router = APIRouter()

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create customer
@router.post("/createcustomer/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED,
             description="Create a new customer and return the created customer object.")
async def create_customer_api(customer: CustomerCreate, db: Session = Depends(get_db)):
    """
    Create a new customer and return the created customer object.
    """
    try:
        return create_customer(db, customer.dict())
    except IntegrityError as e:
        logger.error(f"Integrity error while creating customer: {str(e)}")
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(status_code=400, detail="Customer with this email already exists")
        raise HTTPException(status_code=500, detail="Database error occurred")

# GET customer by ID
@router.get("/{customer_id}/viewcustomer/", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
async def single_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single customer by ID.
    """
    customer = get_customer(db, customer_id)
    if customer is None:
        logger.error(f"Customer ID {customer_id} not found")
        raise HTTPException(status_code=404, detail="Customer ID not found")
    bookings = db.query(Bookings).filter(Bookings.customer_id == customer_id).all()
    quotations = db.query(Quotations).filter(Quotations.customer_id == customer_id).all()

    # Creating the response object with all required fields
    response = CustomerResponse(
        customerr_id=customer.customer_id,
        customer_name=customer.customer_name,  # Adjust according to your actual field name
        email=customer.email,
        mobile=customer.mobile,
        role=customer.role,  # Optional, provide if available
        created_at=customer.created_at,
        updated_at=customer.updated_at,  # Optional, provide if available
        bookings=bookings,  # Assuming these are in the correct format
        quotations=quotations  # Assuming these are in the correct format
    )
    
    return response


# GET all customers
@router.get("/allcustomers", response_model=List[CustomerResponse])
def get_all_customers_api(db: Session = Depends(get_db)):
    """
    Retrieve all customers.
    """
    customers = db.query(Customer).options(joinedload(Customer.bookings)).all()
    return customers

# UPDATE customer by ID
@router.put("/{customer_id}/updatecustomer", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
async def edit_customer_api(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    """
    Update customer information by ID.
    If no fields to update are provided, return existing customer data.
    """
    if not any(value is not None for value in customer.dict().values()):
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Retrieve the existing customer details
    existing_customer = get_customer(db, customer_id)
    if existing_customer is None:
        raise HTTPException(status_code=404, detail="Customer ID not found")
    
    # Update the customer details with provided fields
    updated_customer = update_customer(db, customer_id, customer.dict(exclude_unset=True))
    
    # Return the updated customer details
    return updated_customer



# DELETE customer by ID
@router.delete("/{customer_id}/deletecustomer", status_code=status.HTTP_200_OK)
async def delete_customer_api(customer_id: int, db: Session = Depends(get_db)):
    """
    Delete a customer by ID.
    """
    customer = get_customer(db, customer_id)
    if not customer:
        logger.error(f"Customer ID {customer_id} not found")
        raise HTTPException(status_code=404, detail="Customer not found")
    delete_customer(db, customer_id)
    return {"detail": f"Customer {customer.customer_name} (ID: {customer.customer_id}) deleted successfully"}