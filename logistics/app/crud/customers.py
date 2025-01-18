from sqlalchemy.orm import Session, joinedload
from app.models.customers import Customer, CustomerCategory, CustomerType
from app.models.bookings import Bookings
from app.schemas.customers import CustomerResponse
from app.utils import validate_entry_by_id, log_and_raise_exception, get_entity_by_id, populate_dynamic_entries
from sqlalchemy import or_
from typing import Optional
import logging
from fastapi import HTTPException


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


def get_all_customers(db: Session):
    """
    Retrieves all customers from the database and returns them in the CustomerResponse format.
    """
    try:
        customers = db.query(Customer).all()

        # Log the results of the query
        logging.info(f"Fetched customers: {customers}")

        if not customers:
            logging.info("No customers found, returning empty list.")
            return []  # Return an empty list if no customers are found

        # Return the formatted response as a list
        return [
            CustomerResponse(
                customer_id=customer.customer_id,
                customer_name=customer.customer_name,
                email=customer.email,
                mobile=customer.mobile,
                address=customer.address,  # Add missing fields
                city=customer.city,
                state=customer.state,
                country=customer.country,
                pincode=customer.pincode,
                company=customer.company,  # Ensure all required fields are included
                taxid=customer.taxid,
                licensenumber=customer.licensenumber,
                designation=customer.designation,
                is_active=customer.is_active
            )
            for customer in customers
        ]
    except Exception as e:
        logging.error(f"Error fetching customers: {str(e)}")
        return []  # Ensure returning an empty list in case of an error


def get_customer(db: Session, search_term: str, active: Optional[bool] = True):
    """
    Retrieve customers from the database based on a search term, with additional fields like city, state, country, and pincode.
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

        customers = query.all()
        if customers:
            customer_data = []
            for customer in customers:
                customer_data.append({
                    "customer_id": customer.customer_id,
                    "customer_name": customer.customer_name,
                    "email": customer.email,
                    "mobile": customer.mobile,
                    "address": customer.address,  # Include all the required fields
                    "city": customer.city,
                    "state": customer.state,
                    "country": customer.country,
                    "pincode": customer.pincode,
                    "taxid": customer.taxid,
                    "licensenumber": customer.licensenumber,
                    "designation": customer.designation,
                    "is_active": customer.is_active,
                })
            return customer_data

        return {"detail": "Customer not found"}
    except Exception as e:
        log_and_raise_exception(f"Error searching for customer with term {search_term}: {str(e)}", 500)


def get_customer_booking_list(customer_id: int, db: Session):
    """
    Retrieve a customer with booking list details.
    """
    try:
        # Fetch the customer details
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Fetch the bookings for the given customer
        bookings = db.query(Bookings).filter(Bookings.customer_id == customer_id).all()

        # Format the booking list
        booking_list = [
            {
                "booking_id": booking.booking_id,
                "from_city": booking.city,
                "from_pincode": booking.pincode,
                "to_city": booking.to_city, 
                "to_pincode": booking.to_pincode,
                "type": booking.package_type if hasattr(booking, 'package_type') else "N/A",
                "status": booking.booking_status,
                "action": f"View details of Booking {booking.booking_id}",
            }
            for booking in bookings
        ]
        
        # Return customer and booking list details
        return {
            "customer_name": customer.customer_name,
            "mobile": customer.mobile,  # Assuming the `Customer` table has a `phone_number` column
            "email": customer.email,
            "address": customer.address,
            "city": customer.city,
            "state": customer.state,
            "country": customer.country,
            "pincode": customer.pincode,
            "bookings": booking_list
        }

    except Exception as e:
        logging.error(f"Error fetching booking list for customer {customer_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching booking list: {str(e)}")


def get_customer_booking_details(db: Session, customer_id: int, booking_id: int):
    try:
        # Query the booking with the specified customer_id and booking_id
        booking = db.query(Bookings).filter(Bookings.customer_id == customer_id, Bookings.booking_id == booking_id).first()

        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        # Retrieve the customer details
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Map the result to the Pydantic model for response
        booking_response = {
            "customer_name": customer.customer_name,
            "customer_mobile": customer.mobile,
            "customer_email": customer.email,
            "customer_address": customer.address,
            "customer_city": customer.city,
            "customer_state": customer.state,
            "customer_country": customer.country,
            "customer_pincode": customer.pincode,
            "booking_id": booking.booking_id,
            "from_address": booking.from_address,
            "from_city": booking.city,
            "from_pincode": booking.pincode,
            "to_address": booking.to_address,
            "to_city": booking.to_city,
            "to_pincode": booking.to_pincode,
            "package_details": [
                {
                    "No_of_Packages": booking.package_count,
                    "Pickup_Date": booking.pickup_date,
                    "Pickup_Time": booking.pickup_time,
                }
            ],
            "item_details": [
                {
                    "booking_id": item.booking_id,
                    "item_id": item.item_id,
                    "weight": item.weight,
                    "length": item.length,
                    "width": item.width,
                    "height": item.height,
                    "package_type": item.package_type.name,  # Convert enum to string
                    "cost": item.cost,
                }
                for item in booking.booking_items
            ]
        }

        return booking_response

    except Exception as e:
        logging.error(f"Error fetching booking details for booking_id {booking_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")





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