from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.customers import Customer, CustomerCategory, CustomerType, CustomerBusiness
from app.models.bookings import Bookings
from app.schemas.customers import CustomerUpdateResponse
from app.utils import log_and_raise_exception, populate_dynamic_entries, check_existing_customer
from app.service.customers import create_customer_service, get_all_customers_with_booking_list, get_customer_with_booking_details, verify_corporate_customer, suspend_or_activate_customer
import logging
from datetime import datetime
from typing import Optional


logger = logging.getLogger(__name__)

# Helper functions
def log_success(message: str):
    logging.info(message)

def log_error(message: str, status_code: int):
    logging.error(f"{message} - Status Code: {status_code}")


# CRUD operations for Customer
def create_customer(db: Session, customer_data: dict) -> dict:
    """CRUD operation for creating a customer, calling business logic from create_customer_service."""
    logger.debug(f"Received customer data: {customer_data}")

    try:
        result = create_customer_service(db, customer_data)
        
        if isinstance(result, dict):
            return result
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating customer")
    except HTTPException as e:
        logger.error(f"Error in customer creation: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating customer: {str(e)}")


def get_customer_by_email(db: Session, customer_email: str) -> Customer:
    """Retrieve a customer from the database based on their email."""
    try:
        customer = check_existing_customer(db, customer_email)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        return customer
    except Exception as e:
        log_and_raise_exception(f"Error retrieving customer by email {customer_email}: {str(e)}", 500)


def get_customer_by_id(db: Session, customer_id: int) -> Customer:
    """Retrieve a customer by their ID."""
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()


def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()


def get_customers_and_bookings(db: Session, customer_id: int):
    """Retrieve customer and their bookings based on customer_id."""
    try:
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        bookings = db.query(Bookings).filter(Bookings.customer_id == customer_id).all()

        return customer, bookings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching customer with bookings: {str(e)}")


def get_customer_booking_details(db: Session, customer_id: int, booking_id: int):
    """CRUD layer function that calls the service layer to get booking details."""
    return get_customer_with_booking_details(db, customer_id, booking_id)


def update_customer(db: Session, customer_id: int, customer_data: dict):
    """Update a customer with new data."""
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    
    if customer:
        for key, value in customer_data.items():
            setattr(customer, key, value)
        
        db.commit()
        db.refresh(customer)
        
        return CustomerUpdateResponse(
            customer_id=customer.customer_id,
            customer_name=customer.customer_name,
            customer_email=customer.customer_email,
            customer_mobile=customer.customer_mobile,
            customer_address=customer.customer_address,
            customer_city=customer.customer_city,
            customer_state=customer.customer_state,
            customer_country=customer.customer_country,
            customer_pincode=customer.customer_pincode,
            customer_geolocation=customer.customer_geolocation,
            customer_type=customer.customer_type,
            customer_category=customer.customer_category,
            verification_status=customer.verification_status,
            active_flag=customer.active_flag if customer.active_flag is not None else 0,
        )
    
    raise HTTPException(status_code=404, detail="Customer not found")


def update_customer_status(db: Session, customer: Customer, active_flag: int, notes: Optional[str] = None) -> None:
    """Update customer's active status and notes."""
    try:
        customer.active = active_flag
        if notes is not None:
            customer.notes = notes
        db.commit()
    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error updating customer status: {str(e)}", 500)


def update_customer_verification_status(db: Session, customer: Customer, active_flag: int, verification_status: str) -> None:
    """Update customer's verification status and active flag."""
    try:
        customer.active = active_flag
        customer.status = verification_status
        db.commit()
    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error updating customer verification status: {str(e)}", 500)


def verify_customer_in_crud(db: Session, customer_email: str, verification_status: str) -> dict:
    """Verify corporate customer by email."""
    return verify_corporate_customer(db, customer_email, verification_status)


def soft_delete_customer(db: Session, customer_id: int):
    """Soft delete the customer."""
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer.deleted = True
    customer.deleted_at = datetime.utcnow()
    db.add(customer)
    db.commit()
    return customer


def suspend_or_active_customer_crud(db: Session, customer_email: str, active_flag: int, notes: str):
    """Suspend or activate customer."""
    updated_customer = suspend_or_activate_customer(db, customer_email, active_flag, notes)
    return updated_customer


# Additional functions for populating categories and types
def populate_categories(db: Session):
    """Populate customer categories."""
    categories = [CustomerCategory.tier_1, CustomerCategory.tier_2, CustomerCategory.tier_3]
    try:
        populate_dynamic_entries(db, Customer, categories, 'customer_category')
        log_success("Customer categories populated successfully")
    except Exception as e:
        log_error(f"Error populating categories: {str(e)}", 500)
        raise


def populate_customer_types(db: Session):
    """Populate customer types."""
    types = [CustomerType.individual, CustomerType.corporate]
    try:
        populate_dynamic_entries(db, Customer, types, 'customer_type')
        log_success("Customer types populated successfully")
    except Exception as e:
        log_error(f"Error populating customer types: {str(e)}", 500)
        raise


# Retrieve corporate customer details
def get_corporate_customer_details(db: Session, customer_id: int) -> CustomerBusiness:
    """Retrieve corporate customer business details."""
    return db.query(CustomerBusiness).filter(CustomerBusiness.customer_id == customer_id).first()
