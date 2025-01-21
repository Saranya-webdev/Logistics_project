from sqlalchemy.orm import Session
from app.models.customers import Customer, CustomerCategory, CustomerType, CustomerBusiness
from app.models.bookings import Bookings,BookingItem
from app.schemas.customers import CustomerCreate
from app.models.addressbooks import AddressBook
from app.utils import log_and_raise_exception, get_entity_by_id, populate_dynamic_entries
from sqlalchemy import or_
from typing import Optional
import logging
from fastapi import HTTPException,status
from app.service.customers import  create_customer_service

logger = logging.getLogger(__name__)

# CRUD operation for create customer
def create_customer(db: Session, customer_data: dict) -> dict:
    """CRUD operation for creating a customer, calling business logic from create_customer_service."""
    logger.debug(f"Received customer data: {customer_data}")

    try:
        # Call the business logic for creating a customer
        result = create_customer_service(db, customer_data)
        
        # If the result is a success (dict with customer info), return it.
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


# CRUD operation for get all customers
# def get_all_customers(db: Session):
#     """
#     Retrieves all customers from the database and returns them in the CustomerResponse format.
#     """
#     try:
#         customers = db.query(Customer).all()
#         # Log the results of the query
#         logging.info(f"Fetched customers: {customers}")
#         if not customers:
#             logging.info("No customers found, returning empty list.")
#             return []  # Return an empty list if no customers are found
#         # Return the formatted response as a list
#         return [
#             CustomerResponse(
#                 customer_id=customer.customer_id,
#                 customer_name=customer.customer_name,
#                 email=customer.email,
#                 mobile=customer.mobile,
#                 address=customer.address,  # Add missing fields
#                 city=customer.city,
#                 state=customer.state,
#                 country=customer.country,
#                 pincode=customer.pincode,
#                 company=customer.company,  # Ensure all required fields are included
#                 taxid=customer.taxid,
#                 licensenumber=customer.licensenumber,
#                 designation=customer.designation,
#                 is_active=customer.is_active
#             )
#             for customer in customers
#         ]
#     except Exception as e:
#         logging.error(f"Error fetching customers: {str(e)}")
#         return []  # Ensure returning an empty list in case of an error

# CRUD operation for get customer
# def get_customer(db: Session, search_term: str, active: Optional[bool] = True):
#     """
#     Retrieve customers from the database based on a search term, with additional fields like city, state, country, and pincode.
#     """
#     try:
#         if not search_term:
#             return {"detail": "Search term cannot be empty"}
#         query = db.query(Customer).filter(
#             or_(
#                 Customer.customer_name.ilike(f"%{search_term}%"),
#                 Customer.email.ilike(f"%{search_term}%"),
#                 Customer.mobile.ilike(f"%{search_term}%")
#             )
#         )
#         if active is not None:
#             query = query.filter(Customer.is_active == active)
#         customers = query.all()
#         if customers:
#             customer_data = []
#             for customer in customers:
#                 customer_data.append({
#                     "customer_id": customer.customer_id,
#                     "customer_name": customer.customer_name,
#                     "email": customer.email,
#                     "mobile": customer.mobile,
#                     "address": customer.address,  # Include all the required fields
#                     "city": customer.city,
#                     "state": customer.state,
#                     "country": customer.country,
#                     "pincode": customer.pincode,
#                     "taxid": customer.taxid,
#                     "licensenumber": customer.licensenumber,
#                     "designation": customer.designation,
#                     "is_active": customer.is_active,
#                 })
#             return customer_data
#         return {"detail": "Customer not found"}
#     except Exception as e:
#         log_and_raise_exception(f"Error searching for customer with term {search_term}: {str(e)}", 500)

# # CRUD operation for get customer's booking list
# def get_customer_booking_list(customer_id: int, db: Session):
#     """
#     Retrieve a customer with booking list details.
#     """
#     try:
#         # Fetch the customer details
#         customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
#         if not customer:
#             raise HTTPException(status_code=404, detail="Customer not found")
#         # Fetch the bookings for the given customer
#         bookings = db.query(Bookings).filter(Bookings.customer_id == customer_id).all()
#         # Format the booking list
#         booking_list = []
#         for booking in bookings:
#             # Get the related booking items
#             booking_items = db.query(BookingItem).filter(BookingItem.booking_id == booking.booking_id).all()
#             # For each booking item, get the package type
#             for item in booking_items:
#                 booking_list.append({
#                     "booking_id": booking.booking_id,
#                     "from_city": booking.city,
#                     "from_pincode": booking.pincode,
#                     "to_city": booking.to_city,
#                     "to_pincode": booking.to_pincode,
#                     "type": item.package_type.name if item.package_type else "N/A",  # Access the package_type from BookingItem
#                     "status": booking.booking_status,
#                     "action": f"View details of Booking {booking.booking_id}",
#                 })
#         # Return customer and booking list details
#         return {
#             "customer_name": customer.customer_name,
#             "mobile": customer.mobile,
#             "email": customer.email,
#             "address": customer.address,
#             "city": customer.city,
#             "state": customer.state,
#             "country": customer.country,
#             "pincode": customer.pincode,
#             "bookings": booking_list
#         }
#     except Exception as e:
#         logging.error(f"Error fetching booking list for customer {customer_id}: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Error fetching booking list: {str(e)}")

# CRUD operation for get customer's specific booking details
# def get_customer_booking_details(db: Session, customer_id: int, booking_id: int):
#     try:
#         # Query the booking with the specified customer_id and booking_id
#         booking = db.query(Bookings).filter(Bookings.customer_id == customer_id, Bookings.booking_id == booking_id).first()
#         if not booking:
#             raise HTTPException(status_code=404, detail="Booking not found")
        
#         # Retrieve the customer details
#         customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
#         if not customer:
#             raise HTTPException(status_code=404, detail="Customer not found")
        
#         # Map the result to the Pydantic model for response
#         booking_response = {
#             "customer_name": customer.customer_name,
#             "customer_mobile": customer.mobile,
#             "customer_email": customer.email,
#             "customer_address": customer.address,
#             "customer_city": customer.city,
#             "customer_state": customer.state,
#             "customer_country": customer.country,
#             "customer_pincode": customer.pincode,
#             "booking_id": booking.booking_id,
#             "from_address": booking.from_address,
#             "from_city": booking.city,
#             "from_pincode": booking.pincode,
#             "to_address": booking.to_address,
#             "to_city": booking.to_city,
#             "to_pincode": booking.to_pincode,
#             "package_details": [
#                 {
#                     "No_of_Packages": booking.package_count,
#                     "Pickup_Date": booking.pickup_date,
#                     "Pickup_Time": booking.pickup_time,
#                     "estimated_delivery_date": booking.estimated_delivery_date,

#                     "pickup_date": booking.pickup_date,
#                     "pickup_time": booking.pickup_time,
#                 }
#             ],
#             "item_details": [
#                 {   
#                     "item_id": item.item_id,
#                     "booking_id": item.booking_id,
#                     "weight": item.weight,
#                     "length": item.length,
#                     "width": item.width,
#                     "height": item.height,
#                     "package_type": item.package_type,  # Convert enum to string
#                     "cost": item.cost,
#                     "ratings":item.rating,
#                 }
#                 for item in booking.booking_items
#             ]
#         }
#         return booking_response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# CRUD operation for update customer
# def update_customer(db: Session, customer_id: int, customer_data: dict):
#     """
#     update an existing customer in the database.
#     """
#     try:
#         # Call the service function to handle validation and business logic
#         customer_data = update_customer_service(db, customer_id, customer_data)
#         # Proceed with updating the customer if validation passes
#         existing_customer = db.query(Customer).filter(Customer.id == customer_id).first()
#         if not existing_customer:
#             raise HTTPException(status_code=404, detail="Customer not found")
#         for key, value in customer_data.items():
#             setattr(existing_customer, key, value)
#         db.commit()
#         db.refresh(existing_customer)
#         return existing_customer
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=f"Error updating customer with ID {customer_id}: {str(e)}")
    
# CRUD operation for delete customer
# def delete_customer(db: Session, customer_id: int):
#     """
#     delete a customer from the database.
#     """
#     customer_to_delete = get_entity_by_id(db, Customer, customer_id, 'customer_id')
#     try:
#         db.delete(customer_to_delete)
#         db.commit()
#         return {"detail": f"Customer {customer_to_delete.customer_name} (ID: {customer_to_delete.customer_id}) deleted successfully"}
#     except Exception as e:
#         db.rollback()
#         log_and_raise_exception(f"Error deleting customer with ID {customer_id}: {str(e)}", 500)


def log_success(message: str):
    # Log success message++-
    logging.info(message)

def log_error(message: str, status_code: int):
    # Log error message
    logging.error(f"{message} - Status Code: {status_code}")

def populate_categories(db: Session):
    categories = [CustomerCategory.tier_1, CustomerCategory.tier_2, CustomerCategory.tier_3]
    try:
        populate_dynamic_entries(db, Customer, categories, 'customer_category')  # Pass column name
        log_success("Customer categories populated successfully")
    except Exception as e:
        log_error(f"Error populating categories: {str(e)}", 500)
        raise


def populate_customer_types(db: Session):
    types = [CustomerType.individual, CustomerType.corporate]
    try:
        populate_dynamic_entries(db, Customer, types, 'customer_type')  # Pass column name
        log_success("Customer types populated successfully")
    except Exception as e:
        log_error(f"Error populating customer types: {str(e)}", 500)
        raise

