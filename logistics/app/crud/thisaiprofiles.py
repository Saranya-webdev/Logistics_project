from app.models.thisaiprofiles import Associate, AssociatesCredential
from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException, status
import logging
from app.models.bookings import Bookings
from app.utils.utils import log_and_raise_exception




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
        raise HTTPException(status_code=500, detail="Error creating associate in create_associates_crud")
    

# CRUD operations for create associate'S credentail (Mysql db)
def create_associates_credential(db: Session, associates_id: int, email_id: str, password: str):
    """Inserts a new associates credential into the database."""
    try:
        associates_credential = AssociatesCredential(
            associates_id=associates_id,  
            email_id=email_id,  #  Ensure this matches the associatesCredential table
            password=password  
        )

        db.add(associates_credential)
        db.commit()
        db.refresh(associates_credential)
        return associates_credential
    except Exception as e:
        db.rollback()
        raise Exception(f"Database error in create_associates_credential: {e}")
    

# CRUD operations for create associate'S credentail (Mysql db)
def update_associates_password_crud(db: Session, credential: AssociatesCredential, hashed_password: str):
    """Updates an associate's password in the database."""
    try:
        credential.password = hashed_password  # Update the password field

        db.commit()  # Commit transaction
        db.refresh(credential)  # Refresh instance from DB

        return credential
    except Exception as e:
        db.rollback()  # Rollback in case of failure
        raise Exception(f"Database error while updating password in update_associates_password_crud: {e}")



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
        raise Exception(f"Error updating associate in update_associates_crud: {str(e)}")


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
            detail=f"An error occurred while retrieving associates profile in get_associates_profile_crud: {str(e)}"
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
            detail=f"Error fetching associates profiles in get_associates_profiles_list_crud: {str(e)}"
        )


def get_bookings_by_associate_crud(db: Session, associates_email: str):
    """
    Fetch bookings from the database where booking is placed by an associate.
    """
    try:
        bookings = (
            db.query(Bookings)
            .filter(Bookings.booking_by == associates_email)
            .options(joinedload(Bookings.booking_items))
            .all()
        )

        if not bookings:
            log_and_raise_exception(f"No bookings found for associate with email {associates_email}", 404)

        return bookings

    except Exception as e:
        log_and_raise_exception(f"Error fetching bookings in get_bookings_by_associate_crud: {str(e)}", 500)


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
    try:
        associate = db.query(Associate).filter(Associate.associates_email == associates_email).first()

        if not associate:
            log_and_raise_exception(f"No associate found with email {associates_email}", 404)

        associate.active_flag = active_flag
        associate.remarks = remarks
        db.commit()
        db.refresh(associate)

        return associate

    except Exception as e:
        db.rollback()  # Ensure rollback on failure
        log_and_raise_exception(f"Error updating associate status in suspend_or_activate_associates_crud: {str(e)}", 500)


# CRUD operations for verify associate
def verify_associate_crud(
    db: Session, associates_email: str, associates_verification_status: str, active_flag: int
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
                detail="Associate with the provided email not found in verify_associate_crud."
            )

        # Update the associate's verification status and active flag
        existing_associate.associates_verification_status = associates_verification_status
        existing_associate.active_flag = active_flag

        # Commit the changes to the database
        db.commit()
        db.refresh(existing_associate)

        return existing_associate
    except Exception as e:
        db.rollback()  # Roll back changes if there's an error
        raise Exception(f"Database error while updating associate verification in verify_associate_crud: {str(e)}")

        
