from fastapi import HTTPException, status
from app.models.customers import Customer, CustomerBusiness
from app.models.bookings import Bookings
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging
from datetime import datetime
from app.utils import log_and_raise_exception, populate_dynamic_entries, check_existing_by_email
from app.models.enums import Category, Type
from typing import Optional

logger = logging.getLogger(__name__)

# Helper functions
def log_success(message: str):
    logging.info(message)

def log_error(message: str, status_code: int):
    logging.error(f"{message} - Status Code: {status_code}")

def create_customer(db: Session, customer_data: dict) -> dict:
    """
    Calls the create_customer_service function with error handling.
    """
    from app.service.customers import create_customer_service
    try:
        # Call the create_customer_service function to create a customer
        response = create_customer_service(db, customer_data)
        return response  # Return the response from the service function
    except Exception as e:
        # Handle unexpected errors that may occur during the function call
        return {"message": f"Error in create_customer CRUD operation: {str(e)}"}


def update_customer(db: Session, customer_data: dict) -> dict:
    """
    Calls the update_customer_service function with error handling.
    """
    from app.service.customers import update_customer_service
    try:
        # Call the update_customer_service function to update the customer
        response = update_customer_service(db, customer_data)
        return response  # Return the response from the service function
    except Exception as e:
        # Handle unexpected errors that may occur during the function call
        return {"message": f"Error in update_customer CRUD operation: {str(e)}"}

    

def get_customer_by_email(db: Session, customer_email: str):
    """
    Retrieve a customer by email.
    """
    try:
        return check_existing_by_email(db, "customer_email", customer_email)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving customer by email {customer_email}: {str(e)}"
        )



def get_customer_by_id(db: Session, customer_id: int) -> Customer:
    """Retrieve a customer by their ID."""
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()


def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.customer_id == customer_id).first()

def get_customer_profile_in_crud(db: Session, customer_email: str) -> dict:
    """Fetch customer profile by email with error handling."""
    from app.service.customers import get_customer_profile
    try:
        # Call the service function to get the customer profile
        customer_profile = get_customer_profile(db, customer_email)
        return customer_profile  # Return the profile if found
    except HTTPException as e:
        # Handle HTTPExceptions raised from the service (e.g., customer not found)
        return {
            "message": f"Error: {e.detail}",
            "status_code": e.status_code
        }
    except Exception as e:
        # Catch any other unexpected errors
        return {
            "message": f"Unexpected error: {str(e)}"
        }


def get_all_customers_with_booking_list_in_crud(db: Session) -> list:
    """Fetch all customers along with their booking list summaries with error handling."""
    from app.service.customers import get_all_customers_with_booking_list

    try:
        # Call the service function to get all customers with booking summaries
        customer_list = get_all_customers_with_booking_list(db)
        return customer_list  # Return the list of customers with booking summaries

    except HTTPException as e:
        # If an HTTPException is raised (e.g., no customers found)
        return {
            "message": f"Error: {e.detail}",
            "status_code": e.status_code
        }
    except Exception as e:
        # Catch any other unexpected errors
        return {
            "message": f"Unexpected error: {str(e)}"
        }



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


def get_customer_with_booking_details_in_crud(db: Session, customer_id: int, booking_id: int) -> dict:
    """Fetch customer and booking details with error handling."""
    try:
        from app.service.customers import get_customer_with_booking_details
        # Call the service function to get the customer and booking details
        booking_details = get_customer_with_booking_details(db, customer_id, booking_id)
        return booking_details  # Return the booking details

    except HTTPException as e:
        # If an HTTPException is raised (e.g., booking or customer not found)
        return {
            "message": f"Error: {e.detail}",
            "status_code": e.status_code
        }
    except Exception as e:
        # Catch any other unexpected errors
        return {
            "message": f"Unexpected error: {str(e)}"
        }


def update_customer_status(db: Session, customer: Customer, active_flag: int, remarks: Optional[str] = None) -> None:
    """Update customer's active status and remarks."""
    try:
        customer.active = active_flag
        if remarks is not None:
            customer.remarks = remarks
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
    try:
        from app.service.customers import verify_corporate_customer
        # Call the service function to verify the customer
        result = verify_corporate_customer(db, customer_email, verification_status)
        return result  # Return the result if successful
    except HTTPException as e:
        # Handle HTTPExceptions raised from the service (e.g., customer not found, invalid verification status)
        return {
            "message": f"Error: {e.detail}",
            "status_code": e.status_code
        }
    except Exception as e:
        # Catch any other unexpected errors
        return {
            "message": f"Unexpected error: {str(e)}"
        }



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


def suspend_or_activate_customer_crud(
    db: Session, 
    customer_email: str, 
    active_flag: int, 
    notes: str
) -> dict:
    """Handles the CRUD operation for suspending or activating a customer."""
    from app.service.customers import suspend_or_activate_customer_service

    try:
        # Call the service layer to handle business logic
        response = suspend_or_activate_customer_service(db, customer_email, active_flag, notes)
        return response  # Return the response from the service function
    except HTTPException as e:
        # Handle expected HTTP exceptions (e.g., customer not found or invalid flag)
        return {"message": f"Error: {e.detail}", "status_code": e.status_code}
    except Exception as e:
        # Handle unexpected errors
        return {"message": f"Unexpected error: {str(e)}"}



# Additional functions for populating categories and types
def populate_categories(db: Session):
    """Populate customer categories."""
    categories = [Category.tier_1, Category.tier_2, Category.tier_3]
    try:
        populate_dynamic_entries(db, Customer, categories, 'customer_category')
        log_success("Customer categories populated successfully")
    except Exception as e:
        log_error(f"Error populating categories: {str(e)}", 500)
        raise


def populate_customer_types(db: Session):
    """Populate customer types."""
    types = [Type.individual, Type.corporate]
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