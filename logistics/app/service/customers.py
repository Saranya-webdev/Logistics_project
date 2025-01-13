from app.models.customers import Customer
from app.models.bookings import Bookings
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.crud.customers import get_customer, create_customer, update_customer
from app.utils import log_and_raise_exception, check_duplicate_email_or_mobile
import logging
from sqlalchemy.orm import Session

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def create_customer_service(db, customer_data: dict):
    try:
        existing_customer = check_duplicate_email_or_mobile(db, Customer, customer_data['email'], customer_data['mobile'])
        if existing_customer:
            details = []
            if existing_customer.email == customer_data['email']:
                details.append(f"Email {customer_data['email']} already exists.")
            if existing_customer.mobile == customer_data['mobile']:
                details.append(f"Mobile number {customer_data['mobile']} already exists.")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" ".join(details))
        return create_customer(db, customer_data)
    except IntegrityError as e:
        db.rollback()
        log_and_raise_exception(f"Error creating customer: {str(e)}", status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error creating customer: {str(e)}", 500)


def update_customer_service(db, customer_id: int, customer_data: dict):
    """
    Business logic for updating customer details.
    """
    customer = get_customer(db, customer_id)
    try:
        # Update each attribute of the customer
        for key, value in customer_data.items():
            setattr(customer, key, value)
        
        # Commit changes to the database
        db.commit()
        db.refresh(customer)
        return customer
    except IntegrityError as e:
        # Rollback on error and raise HTTP Exception
        db.rollback()
        log_and_raise_exception(f"Error updating customer: {str(e)}", status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Rollback on any other error
        db.rollback()
        log_and_raise_exception(f"Error updating customer with ID {customer_id}: {str(e)}", 500)
