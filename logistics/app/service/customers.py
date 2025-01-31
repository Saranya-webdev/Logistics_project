from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.customers import Customer, CustomerBusiness
from app.models.bookings import Bookings
from app.models.enums import VerificationStatus, Type
from sqlalchemy.exc import IntegrityError
from app.utils import check_existing_by_email
import logging
import json
from app.crud.customers import create_customer_crud,suspend_or_active_customer_crud,verify_corporate_customer_crud, get_customer_profile_crud, get_customer_profile_list_crud, get_customer_with_booking_details_crud,get_customer_with_booking_list_crud, update_customer_crud
from fastapi.responses import JSONResponse

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
            print(f"json formt : {json.dumps(business_details)}")
            # Return the response with business details for corporate customer
            # return {
            #     "customer_id": new_customer.customer_id,
            #     "customer_name": new_customer.customer_name,
            #     "customer_email": new_customer.customer_email,
            #     "customer_mobile": new_customer.customer_mobile,
            #     "customer_address": new_customer.customer_address,
            #     "customer_city": new_customer.customer_city,
            #     "customer_state": new_customer.customer_state,
            #     "customer_country": new_customer.customer_country,
            #     "customer_pincode": new_customer.customer_pincode,
            #     "customer_geolocation": new_customer.customer_geolocation,
            #     "customer_type": new_customer.customer_type,
            #     "customer_category": new_customer.customer_category,
            #     "verification_status": VerificationStatus.pending,
            #     "remarks": new_customer.remarks,
            #     "active_flag": new_customer.active_flag,
            #     "business_details": json.dumps(business_details),  # Serialized business details
            # }
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
                "verification_status": VerificationStatus.pending.value,
                "remarks": new_customer.remarks,
                "active_flag": new_customer.active_flag,
                # "business_details": business_details,  # Serialized business details
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



def update_customer_service(db: Session, customer_data: dict) -> dict:
    """Business logic for updating a customer's details based on customer email."""


    try:
        # Step 1: Check if the customer exists based on email
        existing_customer = check_existing_by_email(db, Customer, "customer_email", customer_data["customer_email"])
        if not existing_customer:
            return {"message": "No customers found with the given email."}  # Return message if no customer is found

        # Step 2: Exclude fields that shouldn't be updated
        fields_to_exclude = ["verification_status", "customer_category", "remarks"]
        filtered_data = {key: value for key, value in customer_data.items() if key not in fields_to_exclude and value is not None}

        # Step 3: Update the customer's details (without modifying customer_email)
        updated_customer = update_customer_crud(db, existing_customer.customer_email, filtered_data)

        if not updated_customer:
            return {"message": "Error updating customer details."}

        # Step 4: Handle business details for corporate customers
        business_details = None
        if customer_data.get("customer_type") == Type.corporate:
            existing_business = db.query(CustomerBusiness).filter(CustomerBusiness.customer_id == updated_customer.customer_id).first()
            if existing_business:
                # Update business fields if the customer is a business (corporate)
                business_fields = ["tax_id", "license_number", "designation", "company_name"]
                for field in business_fields:
                    if field in customer_data and customer_data[field] is not None:
                        setattr(existing_business, field, customer_data[field])
            else:
                # Create a new business entry if it doesn't exist
                business_data = {field: customer_data.get(field) for field in business_fields if customer_data.get(field)}
                business_data["customer_email"] = updated_customer.customer_email
                new_business = CustomerBusiness(**business_data)
                db.add(new_business)
            business_details = {
                "tax_id": existing_business.tax_id if existing_business else None,
                "license_number": existing_business.license_number if existing_business else None,
                "designation": existing_business.designation if existing_business else None,
                "company_name": existing_business.company_name if existing_business else None
            }

        # Commit changes to the database
        db.commit()

        # Return the updated customer details along with business details
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
            "customer_category": updated_customer.customer_category,  # Include customer category if needed
            "tax_id": existing_business.tax_id,
                "license_number": existing_business.license_number ,
                "designation": existing_business.designation ,
                "company_name": existing_business.company_name 
        }

    except Exception as e:
        logger.error(f"Error in updating customer: {str(e)}")
        db.rollback()
        return {"message": f"Error updating customer: {str(e)}"}



def suspend_or_activate_customer_service(
    db: Session, customer_email: str, active_flag: int, remarks: str
) -> dict:
    """
    Suspend, activate, or set a corporate customer's status to pending.
    Individual customers always have `active_flag = 0` and `verification_status = none`.

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
    customer = db.query(Customer).filter(Customer.customer_email == customer_email).first()

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    # If the customer is an individual, keep status unchanged
    if active_flag == 0:
        customer.active_flag = 0
        customer.verification_status = VerificationStatus.none  # Always None for individuals
    else:
        # Corporate Customer - Update accordingly
        if active_flag == 1:
            customer.active_flag = 1
            customer.verification_status = VerificationStatus.verified  # Verified corporate
        elif active_flag == 2:
            customer.active_flag = 2
            customer.verification_status = VerificationStatus.pending  # Pending corporate

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

    # Ensure only corporate customers are updated
    if existing_customer.active_flag == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification status is only applicable for corporate customers."
        )

    # Update active_flag based on verification_status
    if verification_status == VerificationStatus.verified:
        existing_customer.active_flag = 1
    elif verification_status == VerificationStatus.pending:
        existing_customer.active_flag = 2

    existing_customer.verification_status = verification_status

    # Commit changes
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


def get_customer_with_booking_details_service(db: Session, customer_id: int, booking_id: int):
    """Retrieve a specific booking with its items for a given customer."""
    try:
        # Fetch customer using customer_id
        customer = get_customer_profile_crud(db, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Fetch booking using CRUD function
        booking = get_customer_with_booking_details_crud(db, customer.customer_id, booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        # Check if customer is corporate and fetch business details if applicable
        business_details = {}
        if customer.customer_type == Type.corporate:
            if customer.customer_business:
                business_details = {
                    "tax_id": customer.customer_business.tax_id,
                    "license_number": customer.customer_business.license_number,
                    "designation": customer.customer_business.designation,
                    "company_name": customer.customer_business.company_name
                }
            else:
                raise HTTPException(status_code=404, detail="Corporate details not found for this customer")
        
        # Prepare the response with customer, business, and booking details
        booking_response = {
            "customer_name": customer.customer_name,
            "customer_mobile": customer.customer_mobile,
            "customer_email": customer.customer_email,
            "customer_address": customer.customer_address,
            "customer_city": customer.customer_city,
            "customer_state": customer.customer_state,
            "customer_country": customer.customer_country,
            "customer_pincode": customer.customer_pincode,
            "booking_id": booking.booking_id,
            "from_address": booking.from_address,
            "from_city": booking.from_city,
            "from_pincode": booking.from_pincode,
            "to_address": booking.to_address,
            "to_city": booking.to_city,
            "to_pincode": booking.to_pincode,
            "package_details": {
                "no_of_packages": booking.package_count,
                "pickup_date": booking.pickup_date,
                "pickup_time": booking.pickup_time,
                "estimated_delivery_date": booking.estimated_delivery_date
            },
            "item_details": [
                {
                    "item_id": item.item_id,
                    "weight": item.weight,
                    "package_type": item.package_type.name,
                    "cost": item.cost,
                    "ratings": item.rating,
                }
                for item in booking.items  # Access items directly from the booking relationship
            ],
        }
        
        # Include business details for corporate customers
        if business_details:
            booking_response.update(business_details)
        
        return booking_response
    
    except Exception as e:
        logging.error(f"Error retrieving booking details for customer {customer_id} and booking {booking_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


def get_customer_with_booking_list_service(db: Session, customer_email: str) -> dict:
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
        bookings = get_customer_with_booking_list_crud(db, customer.customer_id)
        print(f"Bookings: {bookings}")

        # Construct list of booking summaries
        booking_summaries = [
    {
        "booking_id": booking.booking_id,
        "from_city": booking.from_city,
        "from_pincode": booking.from_pincode,
        "to_city": booking.to_city,
        "to_pincode": booking.to_pincode,
        "status": booking.status,
        "action": booking.action
    }
    for booking in bookings or []
]


        # Add bookings to response
        response["bookings"] = booking_summaries

        return response  # Return the final response dictionary

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logging.error(f"Error retrieving booking list for customer {customer_email}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

