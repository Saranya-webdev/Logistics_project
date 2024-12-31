from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.customers import CreateCustomer, CustomerResponse
from app.crud.customers import get_customer, get_all_customers, create_customer, update_customer, delete_customer
from app.database import get_db
from typing import Optional
from sqlalchemy.exc import IntegrityError


router = APIRouter()

# Create customer
@router.post("/createcustomer/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer_api(customer: CreateCustomer, db: Session = Depends(get_db)):
    try:
        return create_customer(db, customer.dict())
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Customer already exists")
    except Exception:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

# GET customer by ID
@router.get("/{customer_id}/viewcustomer/", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
async def single_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer(db, customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer ID not found")
    return customer

# GET all customers
@router.get("/allcustomers", response_model=list[CustomerResponse], status_code=status.HTTP_200_OK)
async def get_all_customers_api(db: Session = Depends(get_db)):
    customers = get_all_customers(db)
    if not customers:
        raise HTTPException(status_code=404, detail="No customers found")
    return customers

# UPDATE customer by ID
@router.put("/{customer_id}/updatecustomer", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
async def edit_customer_api(customer_id: int, customer: Optional[CreateCustomer] = None, db: Session = Depends(get_db)):
    if not customer:
        raise HTTPException(status_code=400, detail="Customer data must be provided for update")
    
    updated_customer = update_customer(db, customer_id, customer.dict())
    return updated_customer


# DELETE customer by ID
@router.delete("/{customer_id}/deletecustomer", status_code=status.HTTP_200_OK)
async def delete_customer_api(customer_id: int, db: Session = Depends(get_db)):
    customer = delete_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=400, detail="Customer id was not found")
    return {"detail": "Customer deleted"}

