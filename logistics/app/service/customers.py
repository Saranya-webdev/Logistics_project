from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.customers import Customer, CustomerBusiness, CustomerCredential
from app.models.enums import VerificationStatus, Type
from sqlalchemy.exc import IntegrityError
from app.utils.utils import check_existing_by_email,get_credential_by_id, check_existing_by_id_and_email
import logging
import bcrypt
from app.crud.customers import create_customer_crud,suspend_or_active_customer_crud, get_customer_profile_crud, get_customer_profile_list_crud,get_customer_with_booking_list_crud, update_customer_crud, create_customer_credential, update_customer_password_crud
from typing import Optional


logger = logging.getLogger(__name__)

def create_customer_service(db: Session, customer_data: dict) -> dict:
    """Business logic for creating a customer."""
    try:
        # Check for duplicate email
        existing_customer = check_existing_by_email(
            db, Customer, "customer_email", customer_data["customer_email"]
        )
        if existing_customer:
            return {"message": "Customer with this email already exists"}
        
        # Handle corporate customer logic
        if customer_data["customer_type"] == Type.corporate:
            customer_data["active_flag"] = False  # Default active_flag for corporate customers
            customer_data["verification_status"] = "Pending"
            
            # Extract business-specific fields from customer_data
            business_fields = ["tax_id", "license_number", "designation", "company_name"]
            business_data = {field: customer_data.pop(field, None) for field in business_fields}
            
            # Check for missing business fields
            missing_fields = [field for field in business_fields if not business_data.get(field)]
            if missing_fields:
                return {
                    "message": f"Missing required fields for corporate customer: {', '.join(missing_fields)}"
                }
            print(f"customer data in service: {customer_data}")
            print(f"business data in service : {business_data}")
            # Create the customer in the database (without business fields)
            new_customer, new_business = create_customer_crud(db, customer_data, business_data)
            print(f"new customer in service: {new_customer}")
            print(f"new business in service: {new_business}")
            # Serialize business details into a dictionary
            business_details = None
            if new_business:
                print(f"business id in service: {new_business.business_id}")
                business_details = {
                    "business_id": new_business.business_id,
                    "tax_id": new_business.tax_id,
                    "license_number": new_business.license_number,
                    "designation": new_business.designation,
                    "company_name": new_business.company_name,
                }
            print(f"Business data before commit: {business_data}")
            print(f"Returning business details: {business_details}")

            response_data =  {
                "customer_id": new_customer.customer_id,
                "customer_name": new_customer.customer_name,
                "customer_email": new_customer.customer_email,
                "customer_mobile": new_customer.customer_mobile,
                "customer_address": new_customer.customer_address,
                "customer_city": new_customer.customer_city,
                "customer_state": new_customer.customer_state,
                "customer_country": new_customer.customer_country,
                "customer_pincode": new_customer.customer_pincode,
                "customer_geolocation": new_customer.customer_geolocation,
                "customer_type": new_customer.customer_type.value,
                "customer_category": new_customer.customer_category.value,
                "verification_status": VerificationStatus.Pending.value,
                "remarks": new_customer.remarks,
                "active_flag": new_customer.active_flag,
                "business_id": new_business.business_id,
                    "tax_id": new_business.tax_id,
                    "license_number": new_business.license_number,
                    "designation": new_business.designation,
                    "company_name": new_business.company_name,
            }
            print(f"response data: {response_data}")
            return response_data
        # Handle individual customers (no business details)
        else:
            customer_data["active_flag"] = True  # Default active_flag for individual customers
            customer_data["verification_status"] = "None"

            # Create the customer in the database
            new_customer, new_business = create_customer_crud(db, customer_data)

            # Return the response for individual customers
            return {
                "customer_id": new_customer.customer_id,
                "customer_name": new_customer.customer_name,
                "customer_email": new_customer.customer_email,
                "customer_mobile": new_customer.customer_mobile,
                "customer_address": new_customer.customer_address,
                "customer_city": new_customer.customer_city,
                "customer_state": new_customer.customer_state,
                "customer_country": new_customer.customer_country,
                "customer_pincode": new_customer.customer_pincode,
                "customer_geolocation": new_customer.customer_geolocation,
                "customer_type": new_customer.customer_type,
                "customer_category": new_customer.customer_category,
                "verification_status": new_customer.verification_status,
                "remarks": new_customer.remarks,
                "active_flag": new_customer.active_flag,
                "business_details": None,  # No business details for individual customers
            }

    except IntegrityError as e:
        return {"message": f"Database error: {str(e)}"}
    except Exception as e:
        return {"message": f"Unexpected error while creating customer: {str(e)}"}
    

def create_customer_credential_service(db: Session, customer_id: int, customer_email: str, password: str):
    """Business logic for creating customer credentials"""
    try:
        #  Look up customer using ID and email
        customer = check_existing_by_id_and_email(db, Customer, "customer_id", "customer_email", customer_id, customer_email)
        
        if not customer:
            print("Customer ID and Email do not match. Cannot create credentials.")
            return None  # Or raise an exception

        #  Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        
        return create_customer_credential(db, customer.customer_id, customer.customer_email, hashed_password)

    except Exception as e:
        print(f"Error in service layer: {e}")
        return None
    

def update_customer_password_service(db: Session, customer_id: int, new_password: str):
    """Business logic for updating an associate's password."""
    try:
        # Fetch the credential using the generic function
        credential = get_credential_by_id(db, CustomerCredential, "customer_id", customer_id)

        if not credential:
            raise ValueError("Associate credential not found.")

        # Hash the new password securely
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Call CRUD function with hashed password
        return update_customer_password_crud(db, credential, hashed_password)
    except ValueError as e:
        raise ValueError(str(e))  # Pass custom error
    except Exception as e:
        raise Exception(f"Service error while updating password: {e}")        

# EDIT CUSTOMER DETAILS
def update_customer_service(db: Session, customer_data: dict) -> dict:
    """Business logic for updating a customer's details based on customer email."""
    try:
        # Check if the customer exists based on email
        existing_customer = check_existing_by_email(db, Customer, "customer_email", customer_data["customer_email"])
        if not existing_customer:
            return {"message": "No customers found with the given email."}

        # Exclude fields that shouldn't be updated
        fields_to_exclude = ["verification_status", "remarks"]
        filtered_data = {key: value for key, value in customer_data.items() if key not in fields_to_exclude and value is not None}

        # Update the customer's details (without modifying customer_email)
        result = update_customer_crud(db, existing_customer.customer_email, filtered_data)
        if not result or not result[1]:  
            logger.error(f"update_customer_crud failed. Customer email: {existing_customer.customer_email}, Data: {filtered_data}")
            return {"message": "Error updating customer details."}

        customer_type, updated_customer = result

        # **Ensure existing_business is always defined**
        existing_business = None

        # **Define business_fields to avoid UnboundLocalError**
        business_fields = ["tax_id", "license_number", "designation", "company_name"]

        # Handle business details for corporate customers
        if customer_data.get("customer_type") == Type.corporate:
           existing_business = db.query(CustomerBusiness).filter(
           CustomerBusiness.customer_id == updated_customer.customer_id
           ).first()

           if existing_business:
            # Update business fields if the customer is a corporate entity
               for field in business_fields:
                   if field in customer_data and customer_data[field] is not None:
                      setattr(existing_business, field, customer_data[field])
           else:
        # Create a new business entry if it doesn't exist
               business_data = {field: customer_data.get(field) for field in business_fields if customer_data.get(field)}
        
        # Use customer_id instead of customer_email
               business_data["customer_id"] = updated_customer.customer_id  

               new_business = CustomerBusiness(**business_data)
               db.add(new_business)
               existing_business = new_business  # Assign new business instance


        # Commit changes to the database
        db.commit()

        # **Ensure business_details is valid before returning**
        business_details = {
            "tax_id": getattr(existing_business, "tax_id", None),
            "license_number": getattr(existing_business, "license_number", None),
            "designation": getattr(existing_business, "designation", None),
            "company_name": getattr(existing_business, "company_name", None),
        }

        return {
            "customer_id": updated_customer.customer_id,
            "customer_name": updated_customer.customer_name,
            "customer_email": updated_customer.customer_email,
            "customer_mobile": updated_customer.customer_mobile,
            "customer_address": updated_customer.customer_address,
            "customer_city": updated_customer.customer_city,
            "customer_state": updated_customer.customer_state,
            "customer_country": updated_customer.customer_country,
            "customer_pincode": updated_customer.customer_pincode,
            "customer_geolocation": updated_customer.customer_geolocation,
            "customer_type": updated_customer.customer_type,
            "customer_category": updated_customer.customer_category,
            **business_details  # Unpack business details safely
        }

    except Exception as e:
        logger.error(f"Exception in update_customer_service: {e}", exc_info=True)
        db.rollback()
        return {"message": f"Exception in update_customer_service: {str(e)}"}



def suspend_or_activate_customer_service(
    db: Session, customer_email: str, active_flag: int, remarks: str
) -> dict:
    """
    Suspend, activate, or set a corporate customer's status to pending.
    Individual customers always have `active_flag = 0` and `verification_status = NoneValue`.

    Args:
        db (Session): Database session.
        customer_email (str): Customer's email address.
        active_flag (int): Customer status (0: Individual, 1: Corporate Verified, 2: Corporate Pending).
        remarks (str): Additional remarks.

    Returns:
        dict: Updated customer details.
    """
    # Validate active_flag input
    if active_flag not in [0, 1, 2]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid active flag value. Use 0 (Individual), 1 (Corporate Verified), or 2 (Corporate Pending)."
        )

    # Retrieve the customer
    customer = suspend_or_active_customer_crud(db, customer_email, active_flag, remarks)

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    # Individual Customers (active_flag = 0)
    if active_flag == 0:
        customer.active_flag = 0
        customer.verification_status = VerificationStatus.NoneValue 
    else:
        # Corporate Customers
        customer.active_flag = active_flag 
        if active_flag == 1:
            customer.verification_status = VerificationStatus.Verified 
        elif active_flag == 2 and customer.verification_status != VerificationStatus.Verified:
            customer.verification_status = VerificationStatus.Pending 

    # Update remarks
    customer.remarks = remarks

    # Commit the changes
    db.commit()
    db.refresh(customer)

    # Return updated details
    return {
        "customer_id": customer.customer_id,
        "customer_name": customer.customer_name,
        "customer_email": customer.customer_email,
        "customer_mobile": customer.customer_mobile,
        "customer_address": customer.customer_address,
        "customer_city": customer.customer_city,
        "customer_state": customer.customer_state,
        "customer_country": customer.customer_country,
        "customer_pincode": customer.customer_pincode,
        "customer_geolocation": customer.customer_geolocation,
        "active_flag": customer.active_flag,
        "verification_status": customer.verification_status,
        "remarks": remarks,
    }


def verify_corporate_customer_service(
    db: Session, customer_email: str, verification_status: VerificationStatus
) -> dict:
    """
    Update verification status for corporate customers only.

    Args:
        db (Session): Database session.
        customer_email (str): Customer email.
        verification_status (VerificationStatus): New verification status (verified or pending).

    Returns:
        dict: Updated customer details.
    """
    # Retrieve the customer
    existing_customer = db.query(Customer).filter(Customer.customer_email == customer_email).first()

    if not existing_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    print(f"Customer Type: {existing_customer.customer_type.name}")

    # Ensure only corporate customers are updated
    if existing_customer.customer_type.name.lower() != "corporate":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification status is only applicable for corporate customers."
        )

    # Determine active_flag based on verification_status
    if verification_status == VerificationStatus.Verified:
        existing_customer.active_flag = 1  # Verified
    elif verification_status == VerificationStatus.Pending:
        existing_customer.active_flag = existing_customer.active_flag  # Keep the same

    # Update verification_status
    existing_customer.verification_status = verification_status

    # Commit the changes
    db.commit()
    db.refresh(existing_customer)

    return {
        "customer_id": existing_customer.customer_id,
        "customer_name": existing_customer.customer_name,
        "customer_email": existing_customer.customer_email,
        "customer_mobile": existing_customer.customer_mobile,
        "verification_status": existing_customer.verification_status,
        "remarks": existing_customer.remarks,
        "active_flag": existing_customer.active_flag,
        "message": "Customer verification status updated successfully."
    }



def get_customer_profile_service(db: Session, customer_email: str) -> dict:
    """Retrieve a customer profile from the database based on email, including business details if corporate."""
    try:
        # Fetch the customer from the Customer table
        customer = get_customer_profile_crud(db, customer_email)
        
        # Prepare the base response with common customer fields
        response = {
            "customer_id": customer.customer_id,
            "customer_name": customer.customer_name,
            "customer_mobile": customer.customer_mobile,
            "customer_email": customer.customer_email,
            "customer_address": customer.customer_address,
            "customer_city": customer.customer_city,
            "customer_state": customer.customer_state,
            "customer_country": customer.customer_country,
            "customer_pincode": customer.customer_pincode,
            "customer_geolocation": customer.customer_geolocation,
            "customer_type": customer.customer_type.value,
            "customer_category": customer.customer_category,
            "active_flag": customer.active_flag,
        }

        # If the customer is a corporate customer, include the business details
        if customer.customer_type == Type.corporate and customer.customer_business:
            response.update({
                "business_id": customer.customer_business.business_id,
                "tax_id": customer.customer_business.tax_id,
                "license_number": customer.customer_business.license_number,
                "designation": customer.customer_business.designation,
                "company_name": customer.customer_business.company_name
            })

        return response

    except Exception as e:
        logger.error(f"Error retrieving customer profile: {str(e)}")  # Log error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving customer profile: {str(e)}")
    

def get_customers_list_service(db: Session) -> list:
    """Retrieve a list of customer profiles from the database, including business details if corporate."""
    try:
        # Fetch all customers from the Customer table
        customers = get_customer_profile_list_crud(db)
        
        # Prepare a list to store the customer profiles
        response = []

        for customer in customers:
            # Prepare the base response with common customer fields
            customer_profile = {
                "customer_id": customer.customer_id,
                "customer_name": customer.customer_name,
                "customer_mobile": customer.customer_mobile,
                "customer_email": customer.customer_email,
                "customer_address": customer.customer_address,
                "customer_city": customer.customer_city,
                "customer_state": customer.customer_state,
                "customer_country": customer.customer_country,
                "customer_pincode": customer.customer_pincode,
                "customer_geolocation": customer.customer_geolocation,
                "customer_type": customer.customer_type.value,
                "customer_category": customer.customer_category,
                "active_flag": customer.active_flag,
            }

            # If the customer is a corporate customer, include the business details
            if customer.customer_type == Type.corporate and customer.customer_business:
                customer_profile.update({
                    "tax_id": customer.customer_business.tax_id,
                    "license_number": customer.customer_business.license_number,
                    "designation": customer.customer_business.designation,
                    "company_name": customer.customer_business.company_name
                })

            # Append the customer profile to the response list
            response.append(customer_profile)

        return response

    except Exception as e:
        logger.error(f"Error retrieving customer list: {str(e)}")  # Log error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving customer list: {str(e)}")


def get_customer_with_booking_list_service(db: Session, customer_email: str, booking_id: Optional[int] = None) -> dict:
    """Retrieve all bookings for a given customer identified by their email."""
    try:
        # Fetch the customer from the Customer table (with business details)
        customer = get_customer_profile_crud(db, customer_email)

        # Prepare the base response with customer details
        response = {
            "customer_id": customer.customer_id,
            "customer_name": customer.customer_name,
            "customer_mobile": customer.customer_mobile,
            "customer_email": customer.customer_email,
            "customer_address": customer.customer_address,
            "customer_city": customer.customer_city,
            "customer_state": customer.customer_state,
            "customer_country": customer.customer_country,
            "customer_pincode": customer.customer_pincode,
            "customer_geolocation": customer.customer_geolocation,
            "customer_type": customer.customer_type.value,
            "customer_category": customer.customer_category,
        }

        # If the customer is corporate and has business details, include them
        if customer.customer_type == Type.corporate and customer.customer_business:
            response.update({
                "business_id": customer.customer_business.business_id,
                "tax_id": customer.customer_business.tax_id,
                "license_number": customer.customer_business.license_number,
                "designation": customer.customer_business.designation,
                "company_name": customer.customer_business.company_name
            })

        # Fetch all bookings associated with the customer
        bookings = get_customer_with_booking_list_crud(db, customer.customer_id, booking_id)
        print(f"Bookings: {bookings}")

        # Construct list of booking summaries
        booking_summaries = [
    {
        "booking_id": booking.booking_id,
        "customer_id":booking.customer_id,
        "from_name":booking.from_name,
        "from_email":booking.from_email,
        "from_mobile":booking.from_mobile,
        "from_address":booking.from_address,
        "from_state":booking.from_state,
        "from_city": booking.from_city,
        "from_pincode": booking.from_pincode,
        "from_country":booking.from_country,
        "to_name":booking.to_name,
        "to_email":booking.to_email,
        "to_mobile":booking.to_mobile,
        "to_address":booking.to_address,
        "to_state":booking.to_state,
        "to_pincode": booking.to_pincode,
        "to_city":booking.to_city,
        "to_country":booking.to_country,
        "carrier_plan":booking.carrier_plan,
        "carrier_name":booking.carrier_name,
        "pickup_date":booking.pickup_date,
        "pickup_time":booking.pickup_time.strftime("%H:%M:%S") if booking.pickup_time else None,
        "package_count":booking.package_count,
        "est_cost":booking.est_cost,
        "total_cost":booking.total_cost,
        "est_delivery_date":booking.est_delivery_date,
        "booking_date":booking.booking_date,
        "booking_status": booking.booking_status,
        "booking_items":[
            {   "item_id":item.item_id,
                "booking_id":item.booking_id,
                "item_length": item.item_length,
                "item_weight":item.item_weight,
                "item_height":item.item_height,
                "item_width":item.item_width,
                "package_type":item.package_type,
                "package_cost":item.package_cost
            }
            for item in booking.booking_items
        ]    
    }
    for booking in bookings or []
]
        # Add bookings to response
        response["bookings"] = booking_summaries
        print(f"response from service: {response}")

        return response 

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logging.error(f"Error retrieving booking list for customer {customer_email}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

