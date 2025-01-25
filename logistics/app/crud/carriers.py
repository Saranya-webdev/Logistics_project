from app.models.carriers import Carrier  # Correct import
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

# CRUD operations for carrier
def create_carrier_crud(db: Session, carrier_data: dict) -> dict:
    """CRUD operation for creating a carrier."""
    from app.service.carriers import create_carrier_service

    logger.debug(f"Received carrier data: {carrier_data}")

    try:
        result = create_carrier_service(db, carrier_data)
        
        if isinstance(result, dict):
            return result
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating carrier")
    except HTTPException as e:
        logger.error(f"Error in carrier creation: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating carrier: {str(e)}")


def update_carrier_by_id(db: Session, carrier_id: int, carrier_data: dict) -> dict:
    """Update a carrier's details based on carrier ID."""
    from app.service.carriers import update_carrier_service

    try:
        # Call the update_carrier_service to handle the business logic
        result = update_carrier_service(db, carrier_id, carrier_data)

        # If the result from the service layer contains a message (such as 'No carriers found'), raise HTTPException
        if "message" in result:
            if result["message"] == "No carriers found":
                raise HTTPException(status_code=404, detail="Carrier not found")  # Status code 404 for not found
            else:
                raise HTTPException(status_code=400, detail=result["message"])  # Status code 400 for client errors

        # Return the successful result from the service layer
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating carrier: {str(e)}")  # Status code 500 for server errors


def update_carrier_status(db: Session, carrier: Carrier, active_flag: int, remarks: Optional[str] = None) -> None:
    """Update carrier's active status and remarks."""
    try:
        carrier.active_flag = active_flag
        if remarks is not None:
            carrier.remarks = remarks
        db.commit()
        db.refresh(carrier)  # Ensure the carrier object is updated with new values
    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error updating carrier status: {str(e)}", 500)



def get_carrier_by_mobile(db: Session, carrier_mobile: str) -> Carrier:
    """Retrieve a carrier from the database based on their mobile number."""
    try:
        carrier = db.query(Carrier).filter(Carrier.carrier_mobile == carrier_mobile).first()
        if not carrier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrier not found")
        return carrier
    except Exception as e:
        log_and_raise_exception(f"Error retrieving carrier by mobile {carrier_mobile}: {str(e)}", 500)

def get_carrier_profile_crud(db: Session, carrier_mobile: str) -> dict:
    """Call the service to retrieve a carrier's profile based on mobile number."""
    from app.service.carriers import get_carrier_profile
    try:
        # Call the service function to get the carrier profile
        profile = get_carrier_profile(db, carrier_mobile)
        return profile
    except HTTPException as e:
        # Raise the exception if the carrier is not found
        raise e
    except Exception as e:
        # Log and raise a generic exception for other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving carrier profile: {str(e)}"
        )

def get_carrier_profiles_list_crud(db: Session) -> list:
    """Retrieve a list of all carrier profiles from the service layer."""
    from app.service.carriers import get_carriers_profile_list
    try:
        # Call the service function to get the list of all carrier profiles
        carrier_profiles = get_carriers_profile_list(db)
        return carrier_profiles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching carrier profiles: {str(e)}"
        )


def suspend_or_activate_carrier_crud(db: Session, carrier_mobile: str, active_flag: int, remarks: str):
    """Suspend or activate carrier."""
    from app.service.carriers import suspend_or_activate_carrier
    
    try:
        updated_carrier = suspend_or_activate_carrier(db, carrier_mobile, active_flag, remarks)
        return updated_carrier
    except Exception as e:
        log_and_raise_exception(f"Error in suspend or activate carrier: {str(e)}", 500)


def soft_delete_carrier_crud(db: Session, carrier_id: int):
    """Soft delete the carrier by setting the 'deleted' flag to True."""
    carrier = db.query(Carrier).filter(Carrier.carrier_id == carrier_id).first()
    if not carrier:
        raise HTTPException(status_code=404, detail="Carrier not found")
    
    # Set the deleted flag and mark the deletion time
    carrier.deleted = True
    carrier.deleted_at = datetime.utcnow()
    db.add(carrier)
    db.commit()
    
    return carrier