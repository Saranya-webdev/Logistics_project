from app.models.thisaiprofiles import Associate  # Correct import
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging
from app.utils import log_and_raise_exception  # Correct import
from typing import Optional
from datetime import datetime


logger = logging.getLogger(__name__)

# Helper functions
def log_success(message: str):
    logging.info(message)

def log_error(message: str, status_code: int):
    logging.error(f"{message} - Status Code: {status_code}")

# CRUD operations for associates
def create_associates_crud(db: Session, associates_data: dict) -> dict:
    """CRUD operation for creating a associates."""
    from app.service.thisaiprofiles import create_associates_service

    logger.debug(f"Received associates data: {associates_data}")

    try:
        result = create_associates_service(db, associates_data)
        
        if isinstance(result, dict):
            return result
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating associates")
    except HTTPException as e:
        logger.error(f"Error in associates creation: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating associates: {str(e)}")


def create_associate_credential(db: Session, associate_credential: dict) -> dict:
    """
    Calls the service layer to create the associate credential.
    
    Args:
        db (Session): Database session.
        associate_credential (dict): Credential data.
    
    Returns:
        dict: The result from the service layer.
    
    Raises:
        HTTPException: If an error occurs in the service layer or database operation.
    """
    from app.service.thisaiprofiles import create_associate_credential_service
    try:
        # Call the service layer to create the associate credential
        return create_associate_credential_service(db, associate_credential)
    
    except HTTPException as e:
        # Handle the HTTP exception from service layer
        raise e
    except Exception as e:
        # Rollback any changes if an error occurs
        db.rollback()
        # Raise an HTTPException with a detailed error message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in CRUD layer: {str(e)}"
        )


    
def update_associates_by_id(db: Session, associates_id: int, associates_data: dict) -> dict:
    """Update an associate's details based on associates ID."""
    from app.service.thisaiprofiles import update_associates_service

    try:
        # Call the update_associates_service to handle the business logic
        result = update_associates_service(db, associates_id, associates_data)

        # If the result contains a message (such as 'No associates found'), raise HTTPException
        if "message" in result:
            if result["message"] == "No associates found":
                raise HTTPException(status_code=404, detail="Associates not found")  # Status code 404 for not found
            else:
                raise HTTPException(status_code=400, detail=result["message"])  # Status code 400 for client errors

        # Return the successful result from the service layer
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating associates: {str(e)}")  # Status code 500 for server errors



def update_associates_status(db: Session, associates: Associate, active_flag: int, remarks: Optional[str] = None) -> None:
    """Update associates's active status and remarks."""
    try:
        associates.active_flag = active_flag
        if remarks is not None:
            associates.remarks = remarks
        db.commit()
        db.refresh(associates)  # Ensure the associates object is updated with new values
    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error updating associates status: {str(e)}", 500)



def get_associates_by_mobile(db: Session, associates_mobile: str) -> Associate:
    """Retrieve a associates from the database based on their mobile number."""
    try:
        associates = db.query(Associate).filter(Associate.associates_mobile == associates_mobile).first()
        if not associates:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="associates not found")
        return associates
    except Exception as e:
        log_and_raise_exception(f"Error retrieving associates by mobile {associates_mobile}: {str(e)}", 500)

def get_associates_profile_crud(db: Session, associates_mobile: str) -> dict:
    """Call the service to retrieve a associates's profile based on mobile number."""
    from app.service.thisaiprofiles import get_associates_profile
    try:
        # Call the service function to get the associates profile
        profile = get_associates_profile(db, associates_mobile)
        return profile
    except HTTPException as e:
        # Raise the exception if the associates is not found
        raise e
    except Exception as e:
        # Log and raise a generic exception for other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving associates profile: {str(e)}"
        )

def get_associates_profiles_list_crud(db: Session) -> list:
    """Retrieve a list of all associates profiles from the service layer."""
    from app.service.thisaiprofiles import get_associatess_profile_list
    try:
        # Call the service function to get the list of all associates profiles
        associates_profiles = get_associatess_profile_list(db)
        return associates_profiles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching associates profiles: {str(e)}"
        )


def suspend_or_activate_associates_crud(db: Session, associates_mobile: str, active_flag: int, remarks: str):
    """Suspend or activate associates."""
    from app.service.thisaiprofiles import suspend_or_activate_associates
    
    try:
        updated_associates = suspend_or_activate_associates(db, associates_mobile, active_flag, remarks)
        return updated_associates
    except Exception as e:
        log_and_raise_exception(f"Error in suspend or activate associates: {str(e)}", 500)


def verify_associate_crud(db: Session, associates_mobile: str, verification_status: str) -> dict:
    """
    Calls the verify_associates_service to update the associate's verification status and active flag.

    Args:
        db (Session): Database session.
        associates_mobile (str): Mobile number of the associate.
        verification_status (str): Verification status ('Verified' or 'Not Verified').

    Returns:
        dict: Updated associate details or error message.
    """
    from app.service.thisaiprofiles import verify_associates_service
    
    try:
        # Call the service function to verify the associate and update their details
        return verify_associates_service(db, associates_mobile, verification_status)
    
    except HTTPException as http_exc:
        # Handle known exceptions (e.g., 404 Not Found, 500 Internal Server Error)
        raise http_exc  # Reraise the HTTPException

    except Exception as e:
        # Catch all unexpected exceptions and return a custom error message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while verifying the associate: {str(e)}"
        )


def soft_delete_associates_crud(db: Session, associates_id: int):
    """Soft delete the associates by setting the 'deleted' flag to True."""
    associates = db.query(associates).filter(associates.associates_id == associates_id).first()
    if not associates:
        raise HTTPException(status_code=404, detail="associates not found")
    
    # Set the deleted flag and mark the deletion time
    associates.deleted = True
    associates.deleted_at = datetime.utcnow()
    db.add(associates)
    db.commit()
    
    return associates