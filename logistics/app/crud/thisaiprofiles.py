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


# CRUD operations for create associate
def create_associates_crud(db: Session, associates_data: dict) -> Associate:
    """Create a new associate in the database."""
    try:
        # Create the new associate instance
        new_associate = Associate(**associates_data)

        # Add the associate to the session and commit
        db.add(new_associate)
        db.commit()
        db.refresh(new_associate)

        # Return the newly created associate object
        return new_associate

    except Exception as e:
        logger.error(f"Error in associates CRUD operation: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating associate in database")


# CRUD operations for update associate
def update_associates_crud(db: Session, associates_email: str, associates_data: dict) -> Associate:
    """Update an associate's details based on associates email."""
    try:
        # Query the associate by email
        associate = db.query(Associate).filter(Associate.associates_email == associates_email).first()
        if not associate:
            return None

        # Update the associate's data
        for key, value in associates_data.items():
            if value is not None and hasattr(associate, key):
                setattr(associate, key, value)

        # Commit changes to the database
        db.commit()
        db.refresh(associate)

        return associate

    except Exception as e:
        db.rollback()
        raise Exception(f"Error updating associate in CRUD: {str(e)}")


# CRUD operations for get associate profile
def get_associates_profile_crud(db: Session, associates_email: str) -> dict:
    """Call the service to retrieve a associates's profile based on mobile number."""
    try:
        # Call the service function to get the associates profile
        associate_profile = db.query(Associate).filter(Associate.associates_email == associates_email).first()
        return associate_profile
    
    except HTTPException as e:
        # Raise the exception if the associates is not found
        raise e
    except Exception as e:
        # Log and raise a generic exception for other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving associates profile: {str(e)}"
        )


# CRUD operations for get associate profile list
def get_associates_profiles_list_crud(db: Session) -> list:
    """Retrieve a list of all associates profiles from the service layer."""
    try:
        # Call the service function to get the list of all associates profiles
        associates_profiles = db.query(Associate).all()
        return associates_profiles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching associates profiles: {str(e)}"
        )


# CRUD operations for suspend/active customer
def suspend_or_activate_associates_crud(db: Session, associates_email: str, active_flag: int, remarks: str):
    """
    Suspend or activate an associate directly in the database.

    Args:
        db (Session): Database session.
        associates_email (str): Email of the associate.
        active_flag (int): 1 for activate, 2 for suspend.
        remarks (str): Remarks for the action.

    Returns:
        Associate: The updated associate object.
    """
    associate = db.query(Associate).filter(Associate.associates_email == associates_email).first()

    if not associate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No associate found with the provided email."
        )

    associate.active_flag = active_flag
    associate.remarks = remarks
    db.commit()
    db.refresh(associate)

    return associate


# CRUD operations for verify associate
def verify_associate_crud(
    db: Session, associates_email: str, verification_status: str, active_flag: int
): 
    """
    Verify the associate by email and update their verification status and active flag.
    """
    try:
        # Retrieve the associate using their email
        existing_associate = db.query(Associate).filter(Associate.associates_email == associates_email).first()

        if not existing_associate:
            raise HTTPException(
                status_code=404,
                detail="Associate with the provided email not found."
            )

        # Update the associate's verification status and active flag
        existing_associate.verification_status = verification_status
        existing_associate.active_flag = active_flag

        # Commit the changes to the database
        db.commit()
        db.refresh(existing_associate)

        return existing_associate
    except Exception as e:
        db.rollback()  # Roll back changes if there's an error
        raise Exception(f"Database error while updating associate verification: {str(e)}")

        
