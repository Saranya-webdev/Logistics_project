from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.customers import CreateCustomer, CustomerResponse,UpdateCustomer
from app.crud.customers import get_customer, create_customer, update_customer, delete_customer
from app.database import get_db
from typing import List
from sqlalchemy.exc import IntegrityError
from app.models import Customer
from sqlalchemy.orm import joinedload

router = APIRouter()

# Create customer
@router.post("/createcustomer/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED,
             description="Create a new customer and return the created customer object.")
async def create_customer_api(customer: CreateCustomer, db: Session = Depends(get_db)):

    try:
        # Pass customer data to CRUD function
        return create_customer(db, customer.dict())
    except IntegrityError as e:

        if "UNIQUE constraint failed" in str(e.orig):

            raise HTTPException(status_code=400, detail="Customer with this email already exists")
        raise HTTPException(status_code=500, detail="Database error occurred")

# GET customer by ID
@router.get("/{customer_id}/viewcustomer/", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
async def single_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer(db, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer ID not found")
    return customer

# GET all customers
@router.get("/allcustomers", response_model=List[CustomerResponse])
def get_all_customers_api(db: Session = Depends(get_db)):
    customers = db.query(Customer).options(joinedload(Customer.bookings)).all()
    return customers

# UPDATE customer by ID
@router.put("/{customer_id}/updatecustomer", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
async def edit_customer_api(customer_id: int, customer: UpdateCustomer, db: Session = Depends(get_db)):
    if not any(value is not None for value in customer.dict().values()):
        raise HTTPException(status_code=400, detail="No fields to update")

    updated_customer = update_customer(db, customer_id, customer.dict(exclude_unset=True))
    return updated_customer

# DELETE customer by ID
@router.delete("/{customer_id}/deletecustomer", status_code=status.HTTP_200_OK)
async def delete_customer_api(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    delete_customer(db, customer_id)
    return {"detail": f"Customer {customer.name} (ID: {customer.id}) deleted successfully"}
