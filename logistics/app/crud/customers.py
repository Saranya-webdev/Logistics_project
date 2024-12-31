from sqlalchemy.orm import Session
from app.models import Customer
from fastapi import HTTPException


 # Fetches all customers from the database.
def get_all_customers(db: Session):
    return db.query(Customer).all()


 # Fetches a customer by ID.
def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()

# Creates a new customer in the database.
def create_customer(db: Session, customer_data: dict):
    db_customer = Customer(**customer_data)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


# Updates a customer by ID.
def update_customer(db: Session, customer_id: int, customer_data: dict):
    existing_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not existing_customer:
        raise HTTPException(status_code=404, detail="Customer ID not found")

    # Update fields
    for key, value in customer_data.items():
        setattr(existing_customer, key, value)

    db.commit()
    db.refresh(existing_customer)
    return existing_customer

# Deletes a customer by ID.
def delete_customer(db: Session, customer_id: int):
    delete_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if delete_customer is None:
        raise HTTPException(status_code=404, detail="Customer ID not found")
    
    db.delete(delete_customer)
    db.commit()
    return {"detail": "Customer deleted"}
