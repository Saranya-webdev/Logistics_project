from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.customers import CustomerCreate,  CustomerResponse, CustomerUpdate, CustomerUpdateResponse,CustomerBookingListResponse
from app.models.customers import Customer, CustomerBusiness
from app.databases.mysqldb import get_db
import logging
from app.service.customers import create_customer_service, get_customer_profile
from app.crud.customers import update_customer, get_customers_and_bookings, soft_delete_customer, get_customer, verify_customer_in_crud, suspend_or_active_customer_crud, fetch_all_customers_with_bookings

router = APIRouter() 

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@router.post("/createcustomer/", response_model=CustomerResponse)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """
    Create a new customer in the system. The customer can be either individual or corporate.
    Checks for duplicate email or mobile number before creating the customer.
    If the customer is corporate, business details are also saved.
    """
    try:
        # Check if a customer already exists with the same email or mobile
        existing_customer = db.query(Customer).filter(
            (Customer.customer_email == customer.customer_email) | 
            (Customer.customer_mobile == customer.customer_mobile)
        ).first()

        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer with the same email or mobile already exists."
            )

        # Set the verification status and active_flag based on customer type
        if customer.customer_type == "corporate":
            verification_status = "pending"
            active_flag = 0
        else:  # individual customer
            verification_status = "none"
            active_flag = 1

        # Create customer object
        created_customer = Customer(
            customer_name=customer.customer_name,
            customer_email=customer.customer_email,
            customer_mobile=customer.customer_mobile,
            customer_address=customer.customer_address,
            customer_city=customer.customer_city,
            customer_state=customer.customer_state,
            customer_country=customer.customer_country,
            customer_geolocation=customer.customer_geolocation,
            customer_pincode=customer.customer_pincode,
            customer_type=customer.customer_type,
            customer_category=customer.customer_category,
            verification_status=verification_status,
            active_flag=active_flag,  # Set the correct flag
        )

        # Save the customer to the database
        db.add(created_customer)
        db.commit()
        db.refresh(created_customer)

        # Handle business details for corporate customers
        business_id = None
        if customer.customer_type == "corporate":
            business_data = {
                "customer_id": created_customer.customer_id,
                "tax_id": customer.tax_id,
                "license_number": customer.license_number,
                "designation": customer.designation,
                "company_name": customer.company_name,
            }
            new_business = CustomerBusiness(**business_data)
            db.add(new_business)
            db.commit()
            db.refresh(new_business)
            business_id = new_business.business_id

        # Return the response
        return CustomerResponse(
            customer_id=created_customer.customer_id,
            customer_name=created_customer.customer_name,
            customer_email=created_customer.customer_email,
            customer_mobile=created_customer.customer_mobile,
            customer_address=created_customer.customer_address,
            customer_city=created_customer.customer_city,
            customer_state=created_customer.customer_state,
            customer_country=created_customer.customer_country,
            customer_geolocation=created_customer.customer_geolocation,
            customer_pincode=created_customer.customer_pincode,
            customer_type=created_customer.customer_type,
            customer_category=created_customer.customer_category,
            verification_status=created_customer.verification_status,
            active_flag=created_customer.active_flag,  
            business_id=business_id,
            tax_id=customer.tax_id if customer.customer_type == "corporate" else None,
            license_number=customer.license_number if customer.customer_type == "corporate" else None,
            designation=customer.designation if customer.customer_type == "corporate" else None,
            company_name=customer.company_name if customer.customer_type == "corporate" else None,
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating customer: {str(e)}"
        )


@router.post("/suspend-or-activate-customer")
def suspend_or_activate_customer_route(customer_email: str, active_flag: int, remarks: str, db: Session = Depends(get_db)):
    """
    Suspend or activate a customer based on their email and active_flag.
    The status of the customer is updated along with any remarks provided.
    """
    updated_customer = suspend_or_active_customer_crud(db, customer_email, active_flag, remarks)
    return {"message": "Customer status updated", "customer": updated_customer}


@router.post("/verifycustomer", status_code=status.HTTP_200_OK)
async def verify_customer(
    customer_email: str,
    verification_status: str,
    db: Session = Depends(get_db)
):
    """
    Verify a customer's status by email. The verification status is updated as per the provided status.
    This is used for verifying corporate customers.
    """
    try:
        # Call the verify_customer_in_crud function that wraps verify_corporate_customer
        updated_customer = verify_customer_in_crud(db, customer_email, verification_status)
        return updated_customer
    except HTTPException as e:
        # Forward the exception if any occurs
        raise HTTPException(status_code=e.status_code, detail=e.detail)


@router.get("/{customer_email}/profile", response_model=dict)
def get_customer_profile(
    customer_email: str, db: Session = Depends(get_db)
):
    """
    Retrieve the profile of a customer based on their email.
    If the customer is corporate, additional business details will be provided.
    """
    try:
        profile = get_customer_profile(db, customer_email)
        return profile
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log and re-raise the exception in case of an unexpected error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail=f"An unexpected error occurred: {str(e)}")
    

@router.get("/customerslistbookings", response_model=list)
def get_customers_with_bookings(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all customers with their booking summaries.
    """
    return fetch_all_customers_with_bookings(db)    


# Get customer with booking list
@router.get("/{customer_id}/bookinglist", response_model=CustomerBookingListResponse)
def get_customer_booking_list(customer_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the list of bookings associated with a customer, identified by their customer ID.
    Includes validation for corporate customer details.
    """
    try:
        # Use the new CRUD operation
        customer, bookings = get_customers_and_bookings(db, customer_id)

        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Check and log customer type for debugging
        logging.debug(f"Customer ID: {customer.customer_id} | Type: {customer.customer_type}")

        # If the customer is corporate, ensure business details are not null
        if customer.customer_type == "corporate":
            corporate_details = db.query(CustomerBusiness).filter(CustomerBusiness.customer_id == customer.customer_id).first()
            if not corporate_details or not (corporate_details.tax_id and corporate_details.license_number and corporate_details.company_name and corporate_details.designation):
                raise HTTPException(
                    status_code=400,
                    detail=f"Corporate customer ID {customer.customer_id} must have valid business details."
                )
        else:
            # For non-corporate customers, business fields should not be returned
            corporate_details = None

        # Prepare the booking list summary
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

        # Construct and return the response
        return CustomerBookingListResponse(
            customer_id=customer.customer_id,
            customer_name=customer.customer_name,
            mobile=customer.customer_mobile,
            email=customer.customer_email,
            address=customer.customer_address,
            city=customer.customer_city,
            state=customer.customer_state,
            country=customer.customer_country,
            pincode=customer.customer_pincode,
            bookings=booking_summary,
            business_id=corporate_details.business_id if corporate_details else None,
            tax_id=corporate_details.tax_id if corporate_details else None,
            license_number=corporate_details.license_number if corporate_details else None,
            designation=corporate_details.designation if corporate_details else None,
            company_name=corporate_details.company_name if corporate_details else None,
        )

    except HTTPException as e:
        raise e  # Pass HTTPExceptions as they are
    except Exception as e:
        logging.error(f"Error fetching customer booking list: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching booking list: {str(e)}")


# Get customer booking details
@router.get("/{customer_id}/bookings/{booking_id}")
def get_booking_details(
    customer_id: int,
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve details for a specific booking of a customer identified by their customer ID and booking ID.
    """
    from app.crud.customers import get_customer_booking_details
    try:
        return get_customer_booking_details(db, customer_id, booking_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching booking details.")


# Update customer by ID
@router.put("/{customer_id}/updatecustomer", response_model=CustomerUpdateResponse, status_code=status.HTTP_200_OK)
async def edit_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    """
    Update the details of an existing customer identified by their customer ID.
    Fields are updated only if provided in the request body.
    """
    # Step 1: Check if any fields are provided for update
    if not any(value is not None for value in customer.dict(exclude_unset=True).values()):
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Step 2: Check if the customer exists
    existing_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not existing_customer:
        raise HTTPException(status_code=404, detail="Customer ID not found")
    
    # Step 3: Call the update_customer function to update customer data
    updated_customer = update_customer(db, customer_id, customer.dict(exclude_unset=True))
    
    # Step 4: Return the updated customer response
    return updated_customer


# Delete customer by ID
@router.delete("/{customer_id}/deletecustomer", status_code=status.HTTP_200_OK)
async def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Soft delete a customer identified by their customer ID. 
    The customer is marked as deleted but the record is not removed from the database.
    """
    customer = get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if customer.deleted:
        raise HTTPException(status_code=400, detail="Customer already marked as deleted")
    
    # Proceed with soft delete if customer exists and isn't deleted yet
    soft_delete_customer(db, customer_id)
    return {"detail": f"Customer {customer.customer_name} (ID: {customer.customer_id}) marked as deleted successfully"}


