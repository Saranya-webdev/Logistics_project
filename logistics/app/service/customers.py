from fastapi import HTTPException, status
from app.models.customers import Customer, CustomerBusiness
from app.models.bookings import Bookings
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.utils import check_existing_customer_by_email
import logging

logger = logging.getLogger(__name__)

def create_customer_service(db: Session, customer_data: dict) -> dict:
    """Business logic for creating a customer."""
    from app.crud.customers import create_customer  # Local import to avoid circular import
    from app.models import CustomerBusiness  # Import CustomerBusiness

    try:
        existing_customer = check_existing_customer_by_email(db, customer_data["customer_email"])
        if existing_customer:
            return {"message": "Customer already exists"}

        # Handle corporate customer logic separately
        if customer_data["customer_type"] == "corporate":
            customer_data["active_flag"] = False  # Using active_flag
            customer_data["verification_status"] = "Pending"

            # Extract business-specific fields and remove from customer_data
            business_fields = ["tax_id", "license_number", "designation", "company_name"]
            business_data = {field: customer_data.pop(field, None) for field in business_fields}

            # Create the new customer with customer-specific fields
            new_customer = Customer(**customer_data)
            db.add(new_customer)
            db.commit()
            db.refresh(new_customer)

            # Create the associated business details in the CustomerBusiness table
            if business_data:  # Ensure business data is not empty
                business_data["customer_id"] = new_customer.customer_id
                new_business = CustomerBusiness(**business_data)
                db.add(new_business)
                db.commit()
                db.refresh(new_business)  # Ensure the business is fully created

            # Return the response with customer and business details
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
                "business_details": business_data  # Include business data for corporate customers
            }

        else:
            # For non-corporate customers, set active and verified status
            customer_data["active_flag"] = True  # Using active_flag
            customer_data["verification_status"] = "Verified"

            # Create the new customer
            new_customer = Customer(**customer_data)
            db.add(new_customer)
            db.commit()

            # Return customer data with no business details for non-corporate customers
            return {
                "customer_id": new_customer.customer_id,
                "customer_name": new_customer.customer_name,
                "customer_email": new_customer.customer_email,
                "customer_mobile": new_customer.customer_mobile,
                "customer_address": new_customer.customer_address,
                "customer_city": new_customer.customer_city,
                "customer_state": new_customer.customer_state,
                "customer_country": new_customer.customer_country,
                "customer_type": new_customer.customer_type,
                "customer_category": new_customer.customer_category,
                "verification_status": new_customer.verification_status,
                "business_details": None  # For non-corporate customers
            }

    except IntegrityError as e:
        db.rollback()
        return {"message": f"Database error: {str(e)}"}
    except Exception as e:
        db.rollback()
        return {"message": f"Error creating customer: {str(e)}"}




def update_customer_service(db: Session, customer_data: dict) -> dict:
    """Business logic for updating a customer and their business details."""
    from app.crud.customers import update_customer  # Local import to avoid circular import

    try:
        # Step 1: Check if the customer already exists based on email
        existing_customer = db.query(Customer).filter(Customer.customer_email == customer_data["customer_email"]).first()
        if not existing_customer:
            return {"message": "Customer does not exist"}

        # Step 2: Exclude fields from update (customer_type, customer_category,remarks, verification_status)
        fields_to_exclude = ["customer_type", "customer_category", "remarks", "verification_status"]
        filtered_data = {key: value for key, value in customer_data.items() if key not in fields_to_exclude and value is not None}

        # Step 3: Update main customer details (excluding certain fields)
        for field, value in filtered_data.items():
            if hasattr(existing_customer, field):
                setattr(existing_customer, field, value)

        # Step 4: Handle business details only for corporate customers
        if customer_data.get("customer_type") == "corporate":
            # Update business details if customer is a business (corporate)
            existing_business = db.query(CustomerBusiness).filter(CustomerBusiness.customer_id == existing_customer.customer_id).first()
            if existing_business:
                # Update business fields
                business_fields = ["tax_id", "license_number", "designation", "company_name"]
                for field in business_fields:
                    if field in customer_data and customer_data[field] is not None:
                        setattr(existing_business, field, customer_data[field])
            else:
                # If business details don't exist, create new business entry
                business_data = {field: customer_data.get(field) for field in ["tax_id", "license_number", "designation", "company_name"] if customer_data.get(field)}
                business_data["customer_id"] = existing_customer.id
                new_business = CustomerBusiness(**business_data)
                db.add(new_business)

        # Commit the changes to the database
        db.commit()

        # Return the updated customer details
        return {
            "customer_id": existing_customer.customer_id,
            "customer_name": existing_customer.customer_name,
            "customer_email": existing_customer.customer_email,
            "customer_mobile": existing_customer.customer_mobile,
            "customer_address": existing_customer.customer_address,
            "customer_city": existing_customer.customer_city,
            "customer_state": existing_customer.customer_state,
            "customer_country": existing_customer.customer_country,
            "customer_pincode": existing_customer.customer_pincode,
            "customer_geolocation": existing_customer.customer_geolocation,
            "tax_id": existing_business.tax_id if existing_business else None,
            "license_number": existing_business.license_number if existing_business else None,
            "designation": existing_business.designation if existing_business else None,
            "company_name": existing_business.company_name if existing_business else None,
        }

    except IntegrityError as e:
        db.rollback()
        return {"message": f"Database error: {str(e)}"}
    except Exception as e:
        db.rollback()
        return {"message": f"Error updating customer: {str(e)}"}

    

def suspend_or_activate_customer(
    db: Session, customer_email: str, active_flag: int, remarks: str
) -> dict:
    from app.crud.customers import get_customer_by_email, update_customer_status
    """
    Suspend, activate, or set a customer's status to pending based on the provided active_flag.

    Args:
        db (Session): Database session.
        customer_email (str): Customer's email address.
        active_flag (int): Status to update the customer to (0: Pending, 1: Active, 2: Suspended).
        remarks (str): Additional remarks for the status update.

    Returns:
        dict: Updated customer details with active_flag and verification_status.
    """
    # Validate the active_flag
    if active_flag not in [0, 1, 2]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid active flag value. Use 0 (Pending), 1 (Active), or 2 (Suspended)."
        )

    # Retrieve the customer based on email
    existing_customer = get_customer_by_email(db, customer_email)
    if not existing_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    # Update the customer's status and remarks
    update_customer_status(db, existing_customer, active_flag, remarks)
    db.refresh(existing_customer)

    # Map active_flag to a readable verification status
    verification_status_map = {
        0: "Pending",
        1: "Verified",
        2: "Suspended"
    }
    verification_status = verification_status_map.get(active_flag, "Unknown")

    # Return the updated customer details
    return {
        "customer_id": existing_customer.customer_id,
        "customer_name": existing_customer.customer_name,
        "customer_email": existing_customer.customer_email,
        "customer_mobile": existing_customer.customer_mobile,
        "customer_address": existing_customer.customer_address,
        "customer_city": existing_customer.customer_city,
        "customer_state": existing_customer.customer_state,
        "customer_country": existing_customer.customer_country,
        "customer_pincode": existing_customer.customer_pincode,
        "customer_geolocation": existing_customer.customer_geolocation,
        "active_flag": active_flag,
        "verification_status": verification_status,
        "remarks": remarks
    }



def verify_corporate_customer(db: Session, customer_email: str, verification_status: str) -> dict:
    from app.crud.customers import get_customer_by_email, update_customer_verification_status

    # Validate the verification status
    if verification_status not in ["verified", "pending"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification status. Use 'verified' or 'not pending'.")

    # Step 1: Check if the customer exists based on email
    existing_customer = get_customer_by_email(db, customer_email)
    if not existing_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    # Step 2: Update the active flag and status based on the verification status
    if verification_status == "verified":
        active_flag = 1  # Active
    else:
        active_flag = 0  # Pending

    update_customer_verification_status(db, existing_customer, active_flag, verification_status)

    db.refresh(existing_customer)  # Refresh the state of the customer from the database

    # Step 3: Return the updated customer details
    return {
        "customer_id": existing_customer.customer_id,
        "customer_name": existing_customer.customer_name,
        "customer_email": existing_customer.customer_email,
        "active": existing_customer.active,
        "verification_status": existing_customer.verification_status,
        "message": "Customer verification status updated successfully."
    }

def fetch_customer_profile(db: Session, customer_email: str) -> dict:
    from app.crud.customers import get_customer_by_email, get_corporate_customer_details

    # Step 1: Retrieve the customer details using the email
    customer = get_customer_by_email(db, customer_email)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    # Step 2: Construct the common response fields
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
        "customer_type": customer.customer_type,
        "customer_category": customer.customer_category
    }

    # Step 3: If the customer is corporate, retrieve additional details from CustomerBusiness
    if customer.customer_type == "corporate":
        business_details = get_corporate_customer_details(db, customer.customer_id)
        if business_details:
            response.update({
                "business_id": business_details.business_id,
                "tax_id": business_details.tax_id,
                "license_number": business_details.license_number,
                "designation": business_details.designation,
                "company_name": business_details.company_name
            })
        else:
            response["business_details"] = "No additional business details available"

    return response



def get_all_customers_with_booking_list(db: Session) -> list:
    from app.crud.customers import get_customer_by_id  # Import your customer-related CRUD functions
    from app.models import Customer, Bookings, CustomerBusiness  # Ensure these models are imported
    """
    Retrieve all customers with their booking list summaries.
    Includes business details for corporate customers.
    """
    try:
        # Fetch all customers from the database
        customers = db.query(Customer).all()
        if not customers:
            raise HTTPException(status_code=404, detail="No customers found")

        # Prepare the list to hold customer responses
        customer_list = []

        # Iterate through each customer to prepare the response
        for customer in customers:
            # Fetch detailed information about the customer
            customer_details = get_customer_by_id(db, customer.customer_id)

            response = {
                "customer_id": customer_details.customer_id,
                "customer_name": customer_details.customer_name,
                "customer_mobile": customer_details.customer_mobile,
                "customer_email": customer_details.customer_email,
                "customer_address": customer_details.customer_address,
                "customer_city": customer_details.customer_city,
                "customer_state": customer_details.customer_state,
                "customer_country": customer_details.customer_country,
                "customer_pincode": customer_details.customer_pincode,
                "customer_geolocation": customer_details.customer_geolocation,
                "customer_type": customer_details.customer_type,
                "customer_category": customer_details.customer_category,
            }

            # If the customer is corporate, fetch and include business details from CustomerBusiness table
            if customer_details.customer_type == "corporate":
                # Fetch business details from the CustomerBusiness table
                corporate_details = db.query(CustomerBusiness).filter(CustomerBusiness.customer_id == customer_details.customer_id).first()
                if corporate_details:
                    response.update({
                        "business_id": corporate_details.business_id,
                        "tax_id": corporate_details.tax_id,
                        "license_number": corporate_details.license_number,
                        "designation": corporate_details.designation,
                        "company_name": corporate_details.company_name,
                    })
                else:
                    logging.warning(f"Corporate details not found for customer ID {customer_details.customer_id}")
                    # Add empty values if no corporate details found
                    response.update({
                        "business_id": None,
                        "tax_id": None,
                        "license_number": None,
                        "designation": None,
                        "company_name": None,
                    })
            else:
                # Ensure these fields are set to None for non-corporate customers
                response.update({
                    "business_id": None,
                    "tax_id": None,
                    "license_number": None,
                    "designation": None,
                    "company_name": None,
                })

            # Fetch all bookings associated with the current customer
            bookings = db.query(Bookings).filter(Bookings.customer_id == customer_details.customer_id).all()
            booking_summary = [
                {
                    "booking_id": booking.booking_id,
                    "from_city": booking.from_city,
                    "from_pincode": booking.from_pincode,
                    "to_city": booking.to_city,
                    "to_pincode": booking.to_pincode,
                    "status": booking.booking_status,
                    "action": f"View details of Booking {booking.booking_id}",
                }
                for booking in bookings
            ]
            response["bookings"] = booking_summary

            # Add the customer response to the list
            customer_list.append(response)

        return customer_list

    except Exception as e:
        # Log any error that occurs during the process
        logging.error(f"Error fetching customer list with booking summaries: {str(e)}")
        # Raise an HTTPException with status 500 and the error details
        raise HTTPException(status_code=500, detail=f"Error fetching customer list: {str(e)}")



def get_customer_with_booking_details(db: Session, customer_id: int, booking_id: int):
    from app.models.bookings import BookingItem  # Import BookingItem
    try:
        # Query the booking with the specified customer_id and booking_id
        booking = db.query(Bookings).filter(Bookings.customer_id == customer_id, Bookings.booking_id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        # Retrieve the customer details
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Check if the customer is corporate and fetch additional business details
        business_details = {}
        if customer.customer_type == "corporate":
            corporate_details = db.query(CustomerBusiness).filter(CustomerBusiness.customer_id == customer_id).first()
            if corporate_details:
                business_details = {
                    "business_id": corporate_details.business_id,
                    "tax_id": corporate_details.tax_id,
                    "license_number": corporate_details.license_number,
                    "designation": corporate_details.designation,
                    "company_name": corporate_details.company_name,
                }
            else:
                raise HTTPException(status_code=404, detail="Corporate details not found for this customer")

        # Prepare the booking response with customer, business, and booking details
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
                    "booking_id": item.booking_id,
                    "weight": item.weight,
                    "length": item.length,
                    "width": item.width,
                    "height": item.height,
                    "package_type": item.package_type.name,  # Assuming package_type is an enum
                    "cost": item.cost,
                    "ratings": item.rating,
                }
                for item in db.query(BookingItem).filter(BookingItem.booking_id == booking.booking_id).all()
            ],
        }

        # Include business details for corporate customers
        if business_details:
            booking_response.update(business_details)

        return booking_response

    except Exception as e:
        logging.error(f"Error retrieving booking details for customer {customer_id} and booking {booking_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
