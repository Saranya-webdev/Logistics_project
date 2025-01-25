from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.customers import CustomerCreate,  CustomerResponse, CustomerUpdate, CustomerBookingListResponse
from app.models.customers import CustomerBusiness
from app.databases.mysqldb import get_db
import logging


router = APIRouter() 

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@router.post("/createcustomer/", response_model=CustomerResponse)
async def create_customer_endpoint(customer: CustomerCreate, db: Session = Depends(get_db)):
    """
    Create a new customer in the system. Checks for duplicate email or mobile number before creating.
    Handles corporate or individual customer logic.
    """
    from app.crud.customers import create_customer
    try:
        # Call the CRUD function to handle customer creation logic
        customer_data = customer.dict()  # Convert Pydantic model to dict
        result = create_customer(db, customer_data)

        # Handle case where there was an error during creation
        if "message" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )

        return result  # Return the created customer details

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating customer: {str(e)}"
        )
    


@router.post("/suspend-or-activate-customer")
def suspend_or_activate_customer_route(
    customer_email: str, 
    active_flag: int, 
    remarks: str, 
    db: Session = Depends(get_db)
):
    """
    Suspend or activate a customer based on their email and active_flag.
    The status of the customer is updated along with any remarks provided.
    """
    from app.service.customers import suspend_or_activate_customer_service
    try:
        # Call the service layer to handle business logic
        response = suspend_or_activate_customer_service(db, customer_email, active_flag, remarks)
        return {"message": "Customer status updated", "customer": response}
    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating customer status: {str(e)}"
        )



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
    from app.crud.customers import verify_customer_in_crud
    try:
        # Call the CRUD layer which wraps the service layer
        updated_customer = verify_customer_in_crud(db, customer_email, verification_status)
        
        # Check if the response indicates an error
        if isinstance(updated_customer, dict) and "message" in updated_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=updated_customer["message"]
            )
        
        return updated_customer  # Return the updated customer details

    except HTTPException as e:
        # Forward the exception if any occurs
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@router.get("/{customer_email}/profile", response_model=dict)
def get_customer_profile(
    customer_email: str, db: Session = Depends(get_db)
):
    """
    Retrieve the profile of a customer based on their email.
    If the customer is corporate, additional business details will be provided.
    """
    from app.crud.customers import get_customer_profile_in_crud
    try:
        # Call the CRUD layer to fetch the customer profile
        profile = get_customer_profile_in_crud(db, customer_email)
        
        # If the result contains an error message, raise an HTTPException
        if "message" in profile:
            raise HTTPException(status_code=profile.get("status_code", 400), detail=profile["message"])
        
        return profile  # Return the profile details

    except HTTPException as e:
        # Forward the HTTPException if one occurs
        raise e
    except Exception as e:
        # Log and re-raise the exception in case of an unexpected error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail=f"An unexpected error occurred: {str(e)}")


    

@router.get("/customerslistwithbookings", response_model=list)
def get_customers_with_bookings(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all customers with their booking summaries.
    """
    from app.crud.customers import get_all_customers_with_booking_list_in_crud
    try:
        # Call the CRUD layer to fetch customers with booking summaries
        customer_list = get_all_customers_with_booking_list_in_crud(db)
        
        # If the response contains an error message, raise an HTTPException
        if "message" in customer_list:
            raise HTTPException(status_code=customer_list.get("status_code", 400), detail=customer_list["message"])
        
        return customer_list  # Return the customer list with booking summaries

    except HTTPException as e:
        # Forward the HTTPException if one occurs
        raise e
    except Exception as e:
        # Log and re-raise the exception in case of an unexpected error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail=f"An unexpected error occurred: {str(e)}")
   


# Get customer with booking list
@router.get("/{customer_id}/bookinglist", response_model=CustomerBookingListResponse)
def get_customer_booking_list(customer_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the list of bookings associated with a customer, identified by their customer ID.
    Includes validation for corporate customer details.
    """
    from app.crud.customers import get_customers_and_bookings
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
@router.get("/customer/{customer_id}/booking/{booking_id}", response_model=dict)
def get_customer_with_booking_details(
    customer_id: int, booking_id: int, db: Session = Depends(get_db)
):
    """
    Endpoint to retrieve customer and booking details by customer_id and booking_id.
    Includes customer, booking, and business details (for corporate customers).
    """
    from app.crud.customers import get_customer_with_booking_details_in_crud
    try:
        # Call the CRUD layer to fetch customer and booking details
        booking_details = get_customer_with_booking_details_in_crud(db, customer_id, booking_id)

        # If the response contains an error message, raise an HTTPException
        if "message" in booking_details:
            raise HTTPException(status_code=booking_details.get("status_code", 400), detail=booking_details["message"])

        return booking_details  # Return the booking details response

    except HTTPException as e:
        # Forward the HTTPException if one occurs
        raise e
    except Exception as e:
        # Log and re-raise the exception in case of an unexpected error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail=f"An unexpected error occurred: {str(e)}")



# Update customer by ID
@router.put("/customers/{customer_id}/updatecustomer")
async def edit_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    from app.crud.customers import update_customer
    # Convert Pydantic model to dictionary and exclude unset fields
    customer_data = customer.dict(exclude_unset=True)
    
    # Call the update_customer function
    updated_customer = update_customer(db, customer_id, customer_data)
    
    return updated_customer


# Delete customer by ID
@router.delete("/{customer_id}/deletecustomer", status_code=status.HTTP_200_OK)
async def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Soft delete a customer identified by their customer ID. 
    The customer is marked as deleted but the record is not removed from the database.
    """
    from app.crud.customers import get_customer, soft_delete_customer
    customer = get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if customer.deleted:
        raise HTTPException(status_code=400, detail="Customer already marked as deleted")
    
    # Proceed with soft delete if customer exists and isn't deleted yet
    soft_delete_customer(db, customer_id)
    return {"detail": f"Customer {customer.customer_name} (ID: {customer.customer_id}) marked as deleted successfully"}

