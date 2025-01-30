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

# CRUD operations for create carrier
def create_carrier_crud(db: Session, carrier_data: dict) -> Carrier:
    """
    CRUD operation for creating a carrier in the database.
    """
    try:
        logger.info("Creating carrier in the database...")
        new_carrier = Carrier(**carrier_data)
        db.add(new_carrier)
        db.commit()
        db.refresh(new_carrier)
        return new_carrier
    except Exception as e:
        logger.error(f"Error while creating carrier: {str(e)}")
        db.rollback()
        raise


# CRUD operations for update carrier
def update_carrier_crud(db: Session, carrier_email: str, carrier_data: dict) -> Carrier:
    """Update a carrier's details based on carrier email."""
    try:
        existing_carrier = db.query(Carrier).filter(
            Carrier.carrier_email == carrier_email
        ).first()

        if not existing_carrier:
            raise HTTPException(status_code=404, detail=f"Carrier with email {carrier_email} not found")

        for field, value in carrier_data.items():
            if hasattr(existing_carrier, field) and value is not None:
                setattr(existing_carrier, field, value)

        db.commit()
        db.refresh(existing_carrier)
        return existing_carrier
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating carrier: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating carrier: {str(e)}")


# CRUD operations for get carrier profile
def get_carrier_profile_crud(db: Session, carrier_email: str):
    """
    Retrieve an carrier from the database based on their email.
    """
    try:
        # Query the carrier based on their email
        carrier = db.query(Carrier).filter(Carrier.carrier_email == carrier_email).first()
        return carrier
    except Exception as e:
        raise Exception(f"Database error while retrieving carrier: {str(e)}")


# CRUD operations for get carrier's profile list
def get_all_carriers_list_crud(db: Session):
    """
    Retrieve all carriers from the database.
    """
    try:
        # Query all carriers from the database
        carriers = db.query(Carrier).all()
        return carriers
    except Exception as e:
        # Raise an exception if there's a database error
        raise Exception(f"Database error while retrieving all carriers: {str(e)}")


# CRUD operations for suspen/active carrier
def suspend_or_activate_carrier_crud(db: Session, carrier_email: str, active_flag: int, remarks: str):
    """CRUD operation to suspend or activate a carrier."""
    try:
        # Fetch the carrier by email
        carrier = db.query(Carrier).filter(Carrier.carrier_email == carrier_email).first()
        
        if not carrier:
            return None  # No carrier found

        # Update the carrier's status
        carrier.active_flag = active_flag
        carrier.remarks = remarks

        # Commit the changes to the database
        db.commit()
        db.refresh(carrier)

        return carrier  # Return the updated carrier

    except Exception as e:
        db.rollback()  # Rollback if there is any error
        raise Exception(f"Error in updating carrier status: {str(e)}")
