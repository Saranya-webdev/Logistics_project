from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from app.models.customers import Customer,CustomerBusiness,CustomerCredential
from app.models.enums import  Category, Type
from app.models.bookings import Bookings
from app.utils.utils import  populate_dynamic_entries
import logging


logger = logging.getLogger(__name__)

# Helper functions
def log_success(message: str):
    logging.info(message)

def log_error(message: str, status_code: int):
    logging.error(f"{message} - Status Code: {status_code}")

# CRUD operation for create customer
def create_customer_crud(db: Session, customer_data: dict, business_data: dict = None) -> tuple:
    """Create an individual or corporate customer, including business details if corporate."""
    try:
        # Create the Customer record first
        new_customer = Customer(
            customer_name=customer_data["customer_name"],
            customer_mobile=customer_data["customer_mobile"],
            customer_email=customer_data["customer_email"],
            customer_address=customer_data["customer_address"],
            customer_city=customer_data["customer_city"],
            customer_state=customer_data["customer_state"],
            customer_country=customer_data["customer_country"],
            customer_pincode=customer_data["customer_pincode"],
            customer_geolocation=customer_data.get("customer_geolocation"), 
            customer_type=customer_data["customer_type"],  # Must be 'individual' or 'corporate'
            customer_category=customer_data.get("customer_category")  
        )

        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        print(f"new customer : {new_customer}")

        # Initialize new_business as None
        new_business = None
        print(f"business data in crud file: {business_data}")
        # If the customer is corporate, add business details
        if new_customer.customer_type == Type.corporate and business_data:
            print(f"inside corporate")
            # Ensure all business fields are passed
            required_fields = ["tax_id", "license_number", "designation", "company_name"]
            if all(field in business_data for field in required_fields):
                new_business = CustomerBusiness(
                    customer_id=new_customer.customer_id,
                    tax_id=business_data["tax_id"],
                    license_number=business_data["license_number"],
                    designation=business_data["designation"],
                    company_name=business_data["company_name"]
                )
                db.add(new_business)
                db.commit()
                db.refresh(new_business)  # Refresh the business details
                print(f"business details after commit and refresh: {new_business}")

        return new_customer, new_business

    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Error creating customer: {str(e)}")
    except Exception as e:
        db.rollback()
        raise Exception(f"Unexpected error: {str(e)}")
    
# CRUD operation for create customer's credential    
def create_customer_credential(db: Session, customer_id: int, email_id: str, password: str):
    """Inserts a new customer credential into the database."""
    try:
        customer_credential = CustomerCredential(
            customer_id=customer_id,  
            email_id=email_id,  #  Ensure this matches the CustomerCredential table
            password=password  
        )

        db.add(customer_credential)
        db.commit()
        db.refresh(customer_credential)
        return customer_credential
    except Exception as e:
        db.rollback()
        raise Exception(f"Database error: {e}")
    

# CRUD operation for update customer's password
def update_customer_password_crud(db: Session, credential: CustomerCredential, hashed_password: str):
    """Updates an associate's password in the database."""
    try:
        credential.password = hashed_password  # Update the password field

        db.commit()  # Commit transaction
        db.refresh(credential)  # Refresh instance from DB

        return credential
    except Exception as e:
        db.rollback()  # Rollback in case of failure
        raise Exception(f"Database error while updating password: {e}")     


# CRUD operation for get customer profile
def get_customer_profile_crud(db: Session, customer_email: str):
    """Retrieve a customer's profile from the Customer table by their customer_email."""
    try:
        # Query the Customer table to fetch the customer profile by customer_id
        customer = db.query(Customer).filter(Customer.customer_email == customer_email).first()

        # If the customer is not found, raise a 404 error
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with ID {customer_email} not found"
            )

        # Return the customer profile
        return customer

    except Exception as e:
        # Catch any other exceptions and raise a 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving customer profile: {str(e)}"
        )


# CRUD operation for get customer profile list
def get_customer_profile_list_crud(db: Session) -> list:
    """Retrieve all customers."""
    try:
        # Query the Customer table to fetch all customer profiles
        customers = db.query(Customer).all()

        # Return the customer profiles (empty list if no customers)
        return customers

    except Exception as e:
        # Catch any other exceptions and raise a 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving customer profile: {str(e)}"
        )


# CRUD operation for get customer with booking details
# def get_customer_with_booking_details_crud(db: Session, customer_id: int, booking_id: int):
#     """Fetch a specific booking and its related items for a given customer."""
#     try:

#        return db.query(Bookings).filter(
#         Bookings.customer_id == customer_id,
#         Bookings.booking_id == booking_id
#     ).first()

#     except Exception as e:
#         # Catch any other exceptions and raise a 500 error
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error retrieving customer with booking details: {str(e)}"
#         )


# CRUD operation for get customer's booking list
def get_customer_with_booking_list_crud(db: Session, customer_id: int) -> list:
    """CRUD function to get the customer with thier booking list from the database."""
    try:
       bookings = db.query(Bookings).filter(Bookings.customer_id == customer_id).options(
           joinedload(Bookings.booking_items)
       ).all()
       if not bookings:
         logging.warning(f"No bookings found for customer_id {customer_id}")
       return bookings
    except Exception as e:
        # Catch any other exceptions and raise a 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving customer with thier booking list: {str(e)}"
        )   
       

# CRUD operation for update customer
def update_customer_crud(db: Session, customer_email: str, customer_data: dict):
    """CRUD function to update the customer details in the database."""
    try:
        # Retrieve the customer from the database
        customer = db.query(Customer).filter(Customer.customer_email == customer_email).first()
        if not customer:
            return None

        # Update the customer's details dynamically
        for key, value in customer_data.items():
            setattr(customer, key, value)

        # Commit the transaction
        db.commit()

        # Return the updated customer object
        db.refresh(customer)
        return customer

    except Exception as e:
        db.rollback()  # Rollback in case of an error
        logger.error(f"Error in updating customer in CRUD: {str(e)}")
        return None


# CRUD operation for verify corporate customer
def verify_corporate_customer_crud(db: Session, customer: Customer, active_flag: int, verification_status: str) -> Customer:
    """Update customer's verification status and active flag directly."""
    try:
        # Update the customer directly
        customer.active_flag = active_flag
        customer.verification_status = verification_status
        db.commit()
        db.refresh(customer)

        return customer

    except Exception as e:
        db.rollback()  # Roll back changes if there's an error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error updating customer verification: {str(e)}")


# CRUD operation for suspend/active customer
def suspend_or_active_customer_crud(
    db: Session, customer_email: str, active_flag: int, remarks: str
):
    """Suspend or activate a customer directly."""
    # Retrieve the customer by email
    customer = db.query(Customer).filter(Customer.customer_email == customer_email).first()
    
    if not customer:
        return None  # Return None if the customer is not found

    # Update the customer's status and remarks
    customer.active_flag = active_flag
    customer.remarks = remarks
    db.commit()
    db.refresh(customer)
    
    return customer


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



