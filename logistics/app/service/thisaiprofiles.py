from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.thisaiprofiles import Associate,AssociatesCredential
from app.models.enums import VerificationStatus
from app.utils.utils import check_existing_by_email, check_existing_by_id_and_email,get_credential_by_id
from app.crud.thisaiprofiles import create_associates_crud, update_associates_crud, suspend_or_activate_associates_crud, verify_associate_crud,get_associates_profile_crud,get_associates_profiles_list_crud, create_associates_credential,  update_associates_password_crud,get_bookings_by_associate_crud
import logging
import bcrypt

logger = logging.getLogger(__name__)

def create_associates_service(db: Session, associates_data: dict) -> dict:
    """
    Business logic for creating an associate.
    """
    try:
        logger.info("Validating if the associate already exists...")

        # Check if associate already exists using email
        if check_existing_by_email(db, Associate, "associates_email", associates_data["associates_email"]):
            return {"message": "Associate already exists"}  # Changed to 'associates_email'

        # Ensure all required fields are present
        required_fields = [
            "associates_name", "associates_mobile", "associates_email", "associates_role"
        ]

        missing_fields = [field for field in required_fields if field not in associates_data]

        if missing_fields:
            raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing_fields)}")

        # Set default values for any missing fields
        associates_data["active_flag"] = 0  # Default active_flag to 0

        logger.info("Calling CRUD to create the new associate...")
        # Call CRUD to create associate
        new_associate = create_associates_crud(db, associates_data)

        # If associate is created, return success message
        return {
            "message": "Associate created successfully",
            "associates_id": new_associate.associates_id,
            "associates_name": new_associate.associates_name,
            "associates_mobile": new_associate.associates_mobile,
            "associates_email": new_associate.associates_email,
            "associates_role": new_associate.associates_role,
            "associates_verification_status": new_associate.associates_verification_status,
            "active_flag": new_associate.active_flag
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating associate: {str(e)}")
    

def create_associates_credential_service(db: Session, associates_id: int, associates_email: str, password: str):
    """Business logic for creating Associates credentials"""
    try:
        #  Ensure correct model reference (Use `Associates` instead of `Associate`)
        associates = check_existing_by_id_and_email(db, Associate, "associates_id", "associates_email", associates_id, associates_email)
        
        if not associates:
            print("Associates ID and Email do not match. Cannot create credentials.")
            return None  # Or raise an exception

        #  Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        #  Call the correct function with the found associate's values
        return create_associates_credential(db, associates.associates_id, associates.associates_email, hashed_password)

    except Exception as e:
        print(f"Error in service layer: {e}")
        return None  
    

def update_associates_password_service(db: Session, associates_id: int, new_password: str):
    """Business logic for updating an associate's password."""
    try:
        # Fetch the credential using the generic function
        credential = get_credential_by_id(db, AssociatesCredential, "associates_id", associates_id)

        if not credential:
            raise ValueError("Associate credential not found.")

        # Hash the new password securely
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Call CRUD function with hashed password
        return update_associates_password_crud(db, credential, hashed_password)
    except ValueError as e:
        raise ValueError(str(e))  # Pass custom error
    except Exception as e:
        raise Exception(f"Service error while updating password: {e}")


def update_associates_service(db: Session, associates_email: str, associates_data: dict) -> dict:
    """Business logic for updating an associate's details based on associates email."""
    try:
        # Step 1: Check if an associate exists based on email
        existing_associates = check_existing_by_email(db, Associate, "associates_email", associates_email)
        
        if not existing_associates:
            return {"message": "No associate found with the given email."}

        # Call the CRUD function to update the associate in the database
        updated_associate = update_associates_crud(db, associates_email, associates_data)

        if not updated_associate:
            return {"message": "Failed to update associate."}

        # Return the updated associate details
        return {
            "associates_id": updated_associate.associates_id,
            "associates_name": updated_associate.associates_name,
            "associates_email": updated_associate.associates_email,
            "associates_mobile": updated_associate.associates_mobile,
            "associates_role": updated_associate.associates_role,
            "active_flag": updated_associate.active_flag,
            "remarks": updated_associate.remarks,
            "associates_verification_status": updated_associate.associates_verification_status
        }

    except Exception as e:
        return {"message": f"Error updating associate: {str(e)}"}


def suspend_or_activate_associates_service(db: Session, associates_email: str, active_flag: int, remarks: str) -> dict:
    """
    Suspend or activate an associate based on the active_flag input.
    """
    # Validate input for active_flag to ensure it's 1 or 2
    if active_flag not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="active_flag must be 1 (active) or 2 (suspend)"
        )

    try:
        # Call the CRUD layer to perform the database operation
        updated_associates = suspend_or_activate_associates_crud(db, associates_email, active_flag, remarks)

        # Return response in the expected format
        return {
            "associates_id": updated_associates.associates_id,
            "associates_name": updated_associates.associates_name,
            "associates_email": updated_associates.associates_email,
            "associates_mobile": updated_associates.associates_mobile,
            "associates_role": updated_associates.associates_role.value,  # Enum serialized as string
            "active_flag": updated_associates.active_flag,
            "associates_verification_status": updated_associates.associates_verification_status,
            "remarks": updated_associates.remarks
        }

    except HTTPException as http_exc:
        # Re-raise HTTP exceptions
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating associate status: {str(e)}"
        )

    
def verify_associate_service(db: Session, associates_email: str, associates_verification_status: str) -> dict:
    """
    Service method to verify the associate and update their verification status and active flag.
    """
    try:
        # Ensure verification_status is treated as a string
        verification_status_value = associates_verification_status if isinstance(associates_verification_status, str) else associates_verification_status.value

        # Now compare verification_status with Enum's value
        if verification_status_value.lower() == VerificationStatus.Verified.value:
            active_flag = 1
        else:
            active_flag = 0

        # Call the CRUD function to update the associate's status
        updated_associate = verify_associate_crud(db, associates_email, associates_verification_status, active_flag)

        if not updated_associate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No associate found with the provided email."
            )

        # Return the response with correct structure
        return {

                "associates_id": updated_associate.associates_id,
                "associates_name": updated_associate.associates_name,
                "associates_email": updated_associate.associates_email,
                "associates_mobile": updated_associate.associates_mobile,
                "associates_verification_status": updated_associate.associates_verification_status.value,  # Convert Enum to string
                "active_flag": updated_associate.active_flag,
                "associates_role": updated_associate.associates_role.value,  # Convert Enum to string
                "remarks": updated_associate.remarks,
            }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying associate: {str(e)}"
        )


def get_associates_profile_service(db: Session, associates_email: str) -> dict:
    """Business logic to retrieve an associate's profile by email."""
    
    # Fetch the associate record from CRUD
    associate = get_associates_profile_crud(db, associates_email)
    
    if associate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Associate with email {associates_email} not found"
        )
    
    # Construct response dictionary
    return {
        "associates_id": associate.associates_id,
        "associates_name": associate.associates_name,
        "associates_email": associate.associates_email,
        "associates_mobile": associate.associates_mobile,
        "associates_role": associate.associates_role.value,  # Ensure Enum to string conversion
        "active_flag": associate.active_flag,
        "remarks": associate.remarks
    }


def get_associatess_profile_list(db: Session) -> list:
    """Retrieve a list of all associates profiles."""
    try:
        # Get the list of all associatess from the database without filters
        associates = get_associates_profiles_list_crud(db)  # This will retrieve all associatess

        if not associates:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No associates found."
            )
        
        # Map the associatess to a list of dictionaries (profiles)
        associates_profiles = [
            {
                "associates_id": associates.associates_id,
                "associates_name": associates.associates_name,
                "associates_email": associates.associates_email,
                "associates_mobile": associates.associates_mobile,
                "associates_role": associates.associates_role,
                "active_flag": associates.active_flag,
                "remarks": associates.remarks
            }
            for associates in associates
        ]
        return associates_profiles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving associates profiles: {str(e)}"
        )


def get_bookings_by_associate_service(db, associates_email):
    """
    Retrieves all bookings placed by a specific associate and formats them.
    """
    try:
        bookings = get_bookings_by_associate_crud(db, associates_email)

        if not bookings:
            raise HTTPException(status_code=404, detail="No bookings found for this associate.")

        return {
            "associates_email": associates_email,
            "bookings": [
                {
                    "booking_id": booking.booking_id,
                    "customer_id": booking.customer_id,
                    "booking_by": booking.booking_by,
                    "from_name": booking.from_name,
                    "to_name": booking.to_name,
                    "carrier_name": booking.carrier_name,
                    "pickup_date": booking.pickup_date.strftime("%Y-%m-%d"),
                    "package_count": str(booking.package_count),
                    "total_cost":  str(booking.total_cost),
                    "booking_status": booking.booking_status,
                    "booking_items": [
                        {
                            "item_id": item.item_id,
                            "item_length": item.item_length,
                            "item_weight": item.item_weight,
                            "item_width":item.item_width,
                            "item_height": item.item_height,
                            "package_type": item.package_type,
                        }
                        for item in booking.booking_items
                    ],
                }
                for booking in bookings
            ],
        }

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logging.error(f"Error retrieving bookings by associate {associates_email}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
