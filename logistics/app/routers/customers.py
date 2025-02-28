from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.customers import (
    CustomerCreate, 
    CustomerResponse, 
    CustomerUpdate, 
    CustomerUpdateResponse,
    CustomerBookingListResponse,
    VerifyStatusRequest,
    VerifyStatusResponse,
    SuspendOrActiveRequest,
    SuspendOrActiveResponse,
    CustomerCredentialCreate,
    CustomerCredentialResponse,
    CustomerPasswordUpdate
)
from app.databases.mysqldb import get_db
import logging

from app.service.customers import create_customer_service, suspend_or_activate_customer_service, verify_corporate_customer_service, get_customer_profile_service, get_customers_list_service, get_customer_with_booking_list_service, update_customer_service, create_customer_credential_service, update_customer_password_service
# get_customer_with_booking_details_service,


router = APIRouter() 

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@router.post("/createcustomer/", response_model=CustomerResponse)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        # Call the service layer to handle business logic
        new_customer = create_customer_service(db, customer.dict())
        if "message" in new_customer:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=new_customer["message"])
        return new_customer
    except Exception as e:
        logger.error(f"Error creating customer: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating customer: {str(e)}")
    

@router.post("/customer-credentials/", response_model=CustomerCredentialResponse)
def create_customer_credential(
    customer_data: CustomerCredentialCreate,  
    db: Session = Depends(get_db)
):
    """API to create customer credentials"""
    try:
        customer_credential = create_customer_credential_service(
        db, 
        customer_data.customer_id, 
        customer_data.customer_email, 
        customer_data.password
        )
        if not customer_credential:
          raise HTTPException(status_code=400, detail="Customer ID and Email do not match.")

        return CustomerCredentialResponse(
        customer_credential_id=customer_credential.customer_credential_id,
        customer_id=customer_credential.customer_id,
        email_id=customer_credential.email_id,  
        password=customer_credential.password  #  Consider removing from response for security
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating a customer : {str(e)}"
        )


@router.put("/customer/update-password", response_model=dict)
def update_customer_password(data: CustomerPasswordUpdate, db: Session = Depends(get_db)):
    """API endpoint to update an associate's password."""
    try:
        updated_credential = update_customer_password_service(db, data.customer_id, data.new_password)
        
        return {
            "message": "Password updated successfully",
            "customer_id": updated_credential.customer_id
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    


@router.post("/suspend-or-activate/", response_model=SuspendOrActiveResponse)
async def update_customer_status(
    update_request: SuspendOrActiveRequest,
    db: Session = Depends(get_db)
):
    """
    API to activate or suspend a customer.
    """
    try:
        # Call the service to update customer status
        result = suspend_or_activate_customer_service(
            db, 
            **update_request.dict()
        )
        
        # Return the updated customer details
        return result

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating customer status: {str(e)}"
        )


@router.post("/verifycustomer", response_model=VerifyStatusResponse)
async def update_customer_status(
    update_status: VerifyStatusRequest,
    db: Session = Depends(get_db)
):
    try:
        updated_corporate_customer = verify_corporate_customer_service(
            db, 
            update_status.customer_email,
            update_status.verification_status
        )
        return updated_corporate_customer

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        # General exception handling for unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get("/customer/{customer_email}")
def get_customer_profile(customer_email: str, db: Session = Depends(get_db)):
    """Endpoint to retrieve customer profile by email."""
    try:
        customer_profile = get_customer_profile_service(db, customer_email)
        return customer_profile
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the customer profile")
    

@router.get("/customerprofilelist/")
def get_customer_profile_list(db: Session = Depends(get_db)):
    """Endpoint to retrieve customer profile by email."""
    try:
        customers_profile_list = get_customers_list_service(db)
        return customers_profile_list
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the customers profile list")
   

# Get customer with booking list
@router.get("/{customer_email}/bookinglist", response_model=CustomerBookingListResponse)
def get_customer_booking_list(customer_email: str, db: Session = Depends(get_db)):
    """
    Retrieve the list of bookings for a customer identified by their customer_email.
    Includes validation for corporate customer details.
    """
    try:
        return get_customer_with_booking_list_service(db, customer_email)  # No need to wrap in a dict

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


#  Get customer booking details
# @router.get("/customer/{customer_id}/booking/{booking_id}")
# def get_customer_with_booking_details(
#     customer_id: int, booking_id: int, db: Session = Depends(get_db)
# ):
#     """Retrieve a specific booking with its items for a given customer."""
#     try:
#         # Call the service function to get customer and booking details
#         booking_response = get_customer_with_booking_details_service(db, customer_id, booking_id)
#         return booking_response
    
#     except HTTPException as e:
#         # Specific HTTP exception handling (e.g., 404 errors)
#         raise e
#     except Exception as e:
#         logging.error(f"Error retrieving booking details for customer {customer_id} and booking {booking_id}: {str(e)}")
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


<<<<<<< HEAD
# @router.put("/updatecustomer", response_model=CustomerUpdateResponse, status_code=status.HTTP_200_OK)
# async def update_customer(customer_data: CustomerUpdate, db: Session = Depends(get_db)):
#     """
#     Route for updating an customer's details using the request body.
#     """
#     try:
#        if not customer_data.customer_email:
#          raise HTTPException(status_code=400, detail="customer email is required for update.")

#        customer_data_dict = customer_data.dict()

#        updated_customer = update_customer_service(db, customer_data_dict)

#     except:
#           if "message" in updated_customer:
#            raise HTTPException(status_code=400, detail=updated_customer["message"])

#           return updated_customer

@router.put("/updatecustomer", response_model=CustomerUpdateResponse, status_code=status.HTTP_200_OK)
async def update_customer(customer_data: CustomerUpdate, db: Session = Depends(get_db)):
    """
    Route for updating a customer's details using the request body.
    """
    if not customer_data.customer_email:
        raise HTTPException(status_code=400, detail="Customer email is required for update.")

    customer_data_dict = customer_data.dict()

    try:
        updated_customer = update_customer_service(db, customer_data_dict)
        
        # Ensure the response matches CustomerUpdateResponse
        if not isinstance(updated_customer, dict) or "customer_id" not in updated_customer:
            raise HTTPException(status_code=400, detail="Error updating customer details.")

        return updated_customer

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

=======
@router.put("/updatecustomer", response_model=CustomerUpdateResponse, status_code=status.HTTP_200_OK)
async def update_customer(customer_data: CustomerUpdate, db: Session = Depends(get_db)):
    """
    Route for updating an customer's details using the request body.
    """
    try:
       if not customer_data.customer_email:
         raise HTTPException(status_code=400, detail="customer email is required for update.")

       customer_data_dict = customer_data.dict()

       updated_customer = update_customer_service(db, customer_data_dict)

    except:
          if "message" in updated_customer:
           raise HTTPException(status_code=400, detail=updated_customer["message"])

          return updated_customer
>>>>>>> origin/main
