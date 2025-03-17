from app.models.carriers import Carrier,CarrierAccount 
from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
import logging
from app.utils.utils import log_and_raise_exception 

logger = logging.getLogger(__name__)

# Helper functions
def log_success(message: str):
    logging.info(message)

def log_error(message: str, status_code: int):
    logging.error(f"{message} - Status Code: {status_code}")

# CRUD operations for create carrier
def create_carrier_crud(db: Session, carrier_data: dict) -> Carrier:
    """Create a new carrier entry in the database."""
    try:
        new_carrier = Carrier(
            carrier_name=carrier_data["carrier_name"],
            carrier_email=carrier_data["carrier_email"],
            carrier_mobile=carrier_data["carrier_mobile"],
            carrier_address=carrier_data["carrier_address"],
            carrier_city=carrier_data["carrier_city"],
            carrier_state=carrier_data["carrier_state"],
            carrier_country=carrier_data["carrier_country"],
            carrier_pincode=carrier_data["carrier_pincode"],
            carrier_geolocation=carrier_data["carrier_geolocation"],
            active_flag=carrier_data.get("active_flag", 1)  # Default to 1
        )
        
        db.add(new_carrier)
        db.commit()
        db.refresh(new_carrier)
        return new_carrier

    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error creating carrier in create_carrier_crud: {str(e)}", 500)


# CRUD operations for create carrier with account

def create_carrier_with_account(db: Session, carrier_data, account_data):
    """Create a new carrier and its associated account in the database."""
    try:
        # Create the carrier
        new_carrier = Carrier(**carrier_data)
        db.add(new_carrier)
        db.commit()
        db.refresh(new_carrier)  # Ensure we get the updated carrier details

        # Create the associated carrier account
        new_account = CarrierAccount(
            account_name=account_data["account_name"],
            account_number=account_data["account_number"],
            account_id=account_data["account_id"],
            carrier_id=new_carrier.id  # Associate account with the created carrier
        )

        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        return new_carrier, new_account

    except Exception as e:
        db.rollback()  # Rollback any changes if an error occurs
        log_and_raise_exception(f"Error creating carrier and account in create_carrier_with_account: {str(e)}", 500)




# CRUD operations for update carrier
def update_carrier_crud(db: Session, carrier_email: str, carrier_data: dict) -> Carrier:
    """Update a carrier's details based on carrier email."""
    try:
        existing_carrier = db.query(Carrier).filter(
            Carrier.carrier_email == carrier_email
        ).first()

        if not existing_carrier:
            log_and_raise_exception(f"Carrier with email {carrier_email} not found in update_carrier_crud", 404)

        for field, value in carrier_data.items():
            if hasattr(existing_carrier, field) and value is not None:
                setattr(existing_carrier, field, value)

        db.commit()
        db.refresh(existing_carrier)
        return existing_carrier

    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error updating carrier in update_carrier_crud: {str(e)}", 500)


# CRUD operations for get carrier profile
def get_carrier_profile_crud(db: Session, carrier_email: str):
    """
    Retrieve a carrier along with their account details based on email.
    """
    try:
        return (
            db.query(Carrier)
            .filter(Carrier.carrier_email == carrier_email)
            .options(joinedload(Carrier.account))  # Load the related CarrierAccount
            .first()
        )
    except Exception as e:
        log_and_raise_exception(f"Database error while retrieving carrier in get_carrier_profile_crud: {str(e)}", 500)


# CRUD operations for getting all carriers' profiles
def get_all_carriers_list_crud(db: Session):
    """
    Retrieve all carriers along with their account details.
    """
    try:
        return (
            db.query(Carrier)
            .options(joinedload(Carrier.account))
            .all()
        )
    except Exception as e:
        log_and_raise_exception(f"Database error while retrieving all carriers in get_all_carriers_list_crud: {str(e)}", 500)


# CRUD operations for suspen/active carrier
def suspend_or_activate_carrier_crud(db: Session, carrier_email: str, active_flag: int, remarks: str):
    """CRUD operation to suspend or activate a carrier."""
    try:
        # Fetch the carrier by email
        carrier = db.query(Carrier).filter(Carrier.carrier_email == carrier_email).first()
        
        if not carrier:
            log_and_raise_exception(f"Carrier with email {carrier_email} not found in suspend_or_activate_carrier_crud", 404)

        # Update the carrier's status
        carrier.active_flag = active_flag
        carrier.remarks = remarks

        # Commit the changes to the database
        db.commit()
        db.refresh(carrier)

        return carrier  # Return the updated carrier

    except Exception as e:
        db.rollback()  # Rollback if there is any error
        log_and_raise_exception(f"Error updating carrier status in suspend_or_activate_carrier_crud: {str(e)}", 500)
