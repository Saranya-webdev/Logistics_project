from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.carriers import Carrier
from app.utils import check_existing_by_email
import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

def create_carrier_service(db: Session, carrier_data: dict) -> dict:
    """
    Business logic for creating a carrier.
    """
    try:
        # Log validation process
        logger.info("Validating if the carrier already exists...")

        # Check if carrier already exists using email
        if check_existing_by_email(db, Carrier, "carrier_email", carrier_data["carrier_email"]):
            return {"message": "Carrier already exists"}

        # Ensure all required fields are present (remove remarks from here)
        required_fields = [
            "carrier_name", "carrier_mobile", "carrier_email", "carrier_address",
            "carrier_city", "carrier_state", "carrier_country", "carrier_pincode", 
            "carrier_geolocation"
        ]

        missing_fields = [field for field in required_fields if field not in carrier_data]

        if missing_fields:
            return {"message": f"Missing required fields: {', '.join(missing_fields)}"}

        # Set default values
        carrier_data["active_flag"] = 0  # Default active_flag to 0


        logger.info("Creating new carrier...")
        # Create the new carrier
        new_carrier = Carrier(**carrier_data)
        db.add(new_carrier)
        db.commit()
        db.refresh(new_carrier)

        # Return the created carrier details
        return {
            "message": "Carrier created successfully",
            "carrier_id": new_carrier.carrier_id,
            "carrier_name": new_carrier.carrier_name,
            "carrier_mobile": new_carrier.carrier_mobile,
            **{key: getattr(new_carrier, key) for key in carrier_data.keys()},
        }

    except IntegrityError as e:
        logger.error(f"IntegrityError: {str(e)}")
        db.rollback()
        return {"message": "Database error occurred. Please check input data."}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        db.rollback()
        return {"message": f"Error creating carrier: {str(e)}"}



def update_carrier_service(db: Session, carrier_id: int, carrier_data: dict) -> dict:
    """Business logic for updating a carrier's details based on carrier ID."""
    try:
        # Step 1: Check if the carrier exists based on carrier_id
        existing_carrier = db.query(Carrier).filter(Carrier.carrier_id == carrier_id).first()
        if not existing_carrier:
            return {"message": "No carriers found"}  # Return message if no carrier is found

        # Step 2: Update carrier details with the provided data
        for field, value in carrier_data.items():
            if hasattr(existing_carrier, field) and value is not None:
                setattr(existing_carrier, field, value)

        # Commit changes to the database
        db.commit()
        db.refresh(existing_carrier)

        # Return the updated carrier details
        return {
            "carrier_id": existing_carrier.carrier_id,
            "carrier_name": existing_carrier.carrier_name,
            "carrier_email": existing_carrier.carrier_email,
            "carrier_mobile": existing_carrier.carrier_mobile,
            "carrier_address": existing_carrier.carrier_address,
            "carrier_city": existing_carrier.carrier_city,
            "carrier_state": existing_carrier.carrier_state,
            "carrier_country": existing_carrier.carrier_country,
            "carrier_pincode": existing_carrier.carrier_pincode,
            "carrier_geolocation": existing_carrier.carrier_geolocation,
            "active_flag": existing_carrier.active_flag,
            "remarks": existing_carrier.remarks,
        }

    except IntegrityError as e:
        db.rollback()
        return {"message": f"Database error: {str(e)}"}
    except Exception as e:
        db.rollback()
        return {"message": f"Error updating carrier: {str(e)}"}


def suspend_or_activate_carrier(db: Session, carrier_mobile: str, active_flag: int, remarks: str) -> dict:
    """
    Suspend or activate a carrier based on the active_flag input.

    Args:
        db (Session): Database session.
        carrier_mobile (str): Mobile number of the carrier.
        active_flag (int): 1 for activate, 2 for suspend.
        remarks (str): Remarks or notes for the action.

    Returns:
        dict: Updated carrier details or error message.
    """
    from app.crud.carriers import get_carrier_by_mobile, update_carrier_status
    try:
        # Fetch the carrier by mobile
        existing_carrier = get_carrier_by_mobile(db, carrier_mobile)
        if not existing_carrier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No carrier found with the provided mobile number."
            )

        # Update the carrier's active_flag and remarks
        update_carrier_status(db, existing_carrier, active_flag, remarks)
        db.refresh(existing_carrier)

        # Return the updated carrier details
        return {
            'message': 'Carrier status updated successfully.',
            "carrier": {
                "carrier_id": existing_carrier.carrier_id,
                "carrier_name": existing_carrier.carrier_name,
                "carrier_email": existing_carrier.carrier_email,
                "carrier_mobile": existing_carrier.carrier_mobile,
                "carrier_address": existing_carrier.carrier_address,
                "carrier_city": existing_carrier.carrier_city,
                "carrier_state": existing_carrier.carrier_state,
                "carrier_country": existing_carrier.carrier_country,
                "carrier_pincode": existing_carrier.carrier_pincode,
                "carrier_geolocation": existing_carrier.carrier_geolocation,
                "active_flag": active_flag,
                "remarks": remarks
            }
        }

    except HTTPException as http_exc:
        # Re-raise HTTP exceptions
        raise http_exc
    except Exception as e:
        # Rollback the transaction on error
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating carrier status: {str(e)}"
        )


def get_carrier_profile(db: Session, carrier_mobile: str) -> dict:
    """Retrieve the profile of a carrier based on their mobile number."""
    from app.crud.carriers import get_carrier_by_mobile
    carrier = get_carrier_by_mobile(db, carrier_mobile)
    if carrier:
        return {
            "carrier_id": carrier.carrier_id,
            "carrier_name": carrier.carrier_name,
            "carrier_email": carrier.carrier_email,
            "carrier_mobile": carrier.carrier_mobile,
            "carrier_address": carrier.carrier_address,
            "carrier_city": carrier.carrier_city,
            "carrier_state": carrier.carrier_state,
            "carrier_country": carrier.carrier_country,
            "carrier_pincode": carrier.carrier_pincode,
            "carrier_geolocation": carrier.carrier_geolocation,
            "active_flag": carrier.active_flag,
            "remarks": carrier.remarks
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrier not found"
        )

def get_carriers_profile_list(db: Session) -> list:
    """Retrieve a list of all carrier profiles."""
    try:
        # Get the list of all carriers from the database without filters
        carriers = db.query(Carrier).all()  # This will retrieve all carriers
        
        # Map the carriers to a list of dictionaries (profiles)
        carrier_profiles = [
            {
                "carrier_id": carrier.carrier_id,
                "carrier_name": carrier.carrier_name,
                "carrier_email": carrier.carrier_email,
                "carrier_mobile": carrier.carrier_mobile,
                "carrier_address": carrier.carrier_address,
                "carrier_city": carrier.carrier_city,
                "carrier_state": carrier.carrier_state,
                "carrier_country": carrier.carrier_country,
                "carrier_pincode": carrier.carrier_pincode,
                "carrier_geolocation": carrier.carrier_geolocation,
                "active_flag": carrier.active_flag,
                "remarks": carrier.remarks
            }
            for carrier in carriers
        ]
        return carrier_profiles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving carrier profiles: {str(e)}"
        )


def soft_delete_carrier_service(db: Session, carrier_id: int):
    """Service layer function to soft delete a carrier."""
    from app.crud.carriers import soft_delete_carrier_crud
    try:
        # Call the CRUD function to soft delete the carrier
        deleted_carrier = soft_delete_carrier_crud(db, carrier_id)
        return deleted_carrier
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while trying to soft delete the carrier: {str(e)}"
        )