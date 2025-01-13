from sqlalchemy.orm import Session, joinedload
from app.models.customers import Customer, CustomerCategory, CustomerType
from app.models.bookings import Bookings
from app.utils import validate_entry_by_id, log_and_raise_exception, get_entity_by_id, populate_dynamic_entries
from sqlalchemy import or_
from typing import Optional
import logging

def get_all_customers(db: Session):
    """
    Retrives all customers from the database.
    """
    try:
        return db.query(Customer).options(joinedload(Customer.customer_type)).all()
    except Exception as e:
        log_and_raise_exception(f"Error fetching all customers: {str(e)}", 500)

def get_customer(db: Session, search_term: str, active: Optional[bool] = True):
    """
    Retrive a customer from the database.
    """
    try:
        if not search_term:
            return {"detail": "Search term cannot be empty"}

        query = db.query(Customer).filter(
            or_(
                Customer.customer_name.ilike(f"%{search_term}%"),
                Customer.email.ilike(f"%{search_term}%"),
                Customer.mobile.ilike(f"%{search_term}%")
            )
        )
        if active is not None:
            query = query.filter(Customer.is_active == active)

        customer = query.first()
        if customer:
            return {
                "mobile": customer.mobile,
                "email": customer.email,
                "name": customer.customer_name,
                "city": customer.city,
                "state": customer.state,
                "country": customer.country,
                "pincode": customer.pincode
            }
        return {"detail": "Customer not found"}
    except Exception as e:
        log_and_raise_exception(f"Error searching for customer with term {search_term}: {str(e)}", 500)

def get_customer_booking(customer_id: int, db: Session):
    """
    Retrieve a customer with booking details from the database.
    """
    booking = db.query(Bookings).options(
        joinedload(Bookings.booking_items)
    ).filter(Bookings.customer_id == customer_id).first()

    if booking:
        return {
            "from_name": booking.name,
            "from_address": booking.from_address,
            "city": booking.city,
            "state": booking.state,
            "pincode": booking.pincode,
            "country": booking.country,
            "to_name": booking.to_name,
            "to_address": booking.to_address,
            "to_city": booking.to_city,  # Fixed repetition of 'city'
            "to_state": booking.to_state,  # Fixed repetition of 'state'
            "to_pincode": booking.to_pincode,  # Fixed repetition of 'pincode'
            "to_country": booking.to_country,  # Fixed repetition of 'country'
            "booking_items": [
                {
                    "length": item.length,
                    "height": item.height,
                    "weight": item.weight,
                    "width": item.width,
                    "package_type": item.package_type,
                    "cost": item.cost,
                    "estimated_delivery_date": booking.estimated_delivery_date,
                } for item in booking.booking_items
            ],
            "package_details": [
                {
                    "No.of Packages": booking.package_count,
                    "Pickup Date": booking.pickup_date,
                    "Pickup Time": booking.pickup_time
                }
            ]
        }
    return None


def create_customer(db: Session, customer_data: dict):
    """
    Create a new customer in the database.
    """
    try:
        if 'category_id' not in customer_data or 'type_id' not in customer_data:
            raise ValueError("Missing category_id or type_id in customer data")

        validate_entry_by_id(customer_data['category_id'], db, CustomerCategory, 'id')
        validate_entry_by_id(customer_data['type_id'], db, CustomerType, 'id')

        db_customer = Customer(**customer_data)
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error creating customer: {str(e)}", 500)

def update_customer(db: Session, customer_id: int, customer_data: dict):
    """
    update an existing customer in the database.
    """
    existing_customer = get_entity_by_id(db, Customer, customer_id, 'customer_id')
    try:
        if 'category_id' in customer_data:
            validate_entry_by_id(customer_data['category_id'], db, CustomerCategory, 'id')

        if 'type_id' in customer_data:
            validate_entry_by_id(customer_data['type_id'], db, CustomerType, 'id')

        for key, value in customer_data.items():
            setattr(existing_customer, key, value)

        db.commit()
        db.refresh(existing_customer)
        return existing_customer
    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error updating customer with ID {customer_id}: {str(e)}", 500)

def delete_customer(db: Session, customer_id: int):
    """
    delete a customer from the database.
    """
    customer_to_delete = get_entity_by_id(db, Customer, customer_id, 'customer_id')
    try:
        db.delete(customer_to_delete)
        db.commit()
        return {"detail": f"Customer {customer_to_delete.customer_name} (ID: {customer_to_delete.customer_id}) deleted successfully"}
    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error deleting customer with ID {customer_id}: {str(e)}", 500)


def log_success(message: str):
    # Log success message++-
    logging.info(message)

def log_error(message: str, status_code: int):
    # Log error message
    logging.error(f"{message} - Status Code: {status_code}")

def populate_categories(db: Session):
    categories = ["individual", "company", "business", "customs_agent", "carrier"]
    try:
        # Populate categories
        populate_dynamic_entries(db, CustomerCategory, categories)
        # Log success message
        log_success("Customer categories populated successfully")
    except Exception as e:
        # Log error message
        log_error(f"Error populating categories: {str(e)}", 500)
        # Raise the exception after logging the error
        raise

def populate_customer_types(db: Session):
    types = ["regular", "premium", "enterprise", "freelancer", "agency"]
    try:
        # Populate customer types
        populate_dynamic_entries(db, CustomerType, types)
        # Log success message
        log_success("Customer types populated successfully")
    except Exception as e:
        # Log error message
        log_error(f"Error populating customer types: {str(e)}", 500)
        # Raise the exception after logging the error
        raise