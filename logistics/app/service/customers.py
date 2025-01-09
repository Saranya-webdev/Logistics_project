from app.models.customers import Customer
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

def check_customer_exists(db, customer_id: int):
    """
    Check if the customer exists by ID.
    """
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer with ID {customer_id} does not exist.")
    return customer

def create_customer(db, customer_data: dict):
    """
    Business logic for creating a new customer.
    Checks if email or mobile number already exists in the database.
    """
    # Check if the email already exists
    existing_email = db.query(Customer).filter(Customer.email == customer_data['email']).first()
    
    # Check if the mobile number already exists
    existing_mobile = db.query(Customer).filter(Customer.mobile == customer_data['mobile']).first()

    # If both email and mobile number exist, raise an exception
    if existing_email and existing_mobile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Customer with email {customer_data['email']} and mobile number {customer_data['mobile']} already exist."
        )
    
    # If only email exists, raise an exception
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Customer with email {customer_data['email']} already exists."
        )
    
    # If only mobile exists, raise an exception
    if existing_mobile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Customer with mobile number {customer_data['mobile']} already exists."
        )
    
    # Proceed with creating the new customer if neither email nor mobile number exists
    try:
        new_customer = Customer(**customer_data)
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        return new_customer
    except IntegrityError as e:
        db.rollback()  # Rollback the transaction in case of an integrity error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating customer: {str(e)}")

def update_customer(db, customer_id: int, customer_data: dict):
    """
    Business logic for updating customer details.
    """
    customer = check_customer_exists(db, customer_id)
    for key, value in customer_data.items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer
