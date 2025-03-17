from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.carriers import Carrier
from app.utils.utils import check_existing_by_email
import logging
from fastapi import HTTPException, status
from app.crud.carriers import create_carrier_crud, update_carrier_crud, suspend_or_activate_carrier_crud, get_carrier_profile_crud, get_all_carriers_list_crud, create_carrier_with_account


logger = logging.getLogger(__name__)

def create_carrier_service(db: Session, carrier_data: dict) -> dict:
    """
    Business logic for creating a carrier with an associated carrier account.
    """
    try:
        logger.info("Validating if the carrier already exists...")

        # Check if carrier already exists using email
        if check_existing_by_email(db, Carrier, "carrier_email", carrier_data["carrier_email"]):
            return {"message": "Carrier already exists"}

        # Validate required fields for Carrier
        required_carrier_fields = [
            "carrier_name", "carrier_mobile", "carrier_email", "carrier_address",
            "carrier_city", "carrier_state", "carrier_country", "carrier_pincode",
            "carrier_geolocation"
        ]
        missing_carrier_fields = [field for field in required_carrier_fields if field not in carrier_data]
        if missing_carrier_fields:
            return {"message": f"Missing required carrier fields: {', '.join(missing_carrier_fields)}"}

        # Validate required fields for CarrierAccount
        required_account_fields = ["account_name", "account_number"]
        missing_account_fields = [field for field in required_account_fields if field not in carrier_data]
        if missing_account_fields:
            return {"message": f"Missing required carrier account fields: {', '.join(missing_account_fields)}"}

        # Set default values
        carrier_data["active_flag"] = 0  # Default active_flag to 0

        logger.info("Calling CRUD function to create the carrier...")
        # Call the CRUD function to create the carrier
        new_carrier = create_carrier_crud(db, carrier_data)

        # Create a Carrier Account entry
        carrier_account_data = {
            "carrier_id": new_carrier.carrier_id,
            "carrier_name": new_carrier.carrier_name,
            # "carrier_plan": carrier_data["carrier_plan"],
            "account_name": carrier_data["account_name"],
            "account_number": carrier_data["account_number"],
            # "address": carrier_data["carrier_address"],  # Assuming address is the same
            "active_flag": 1  # Default active_flag for carrier account
        }
        new_carrier_account = create_carrier_with_account(db, carrier_account_data)

        # Prepare response
        return {
            "message": "Carrier and carrier account created successfully",
            "carrier_id": new_carrier.carrier_id,
            "carrier_name": new_carrier.carrier_name,
            "carrier_mobile": new_carrier.carrier_mobile,
            "carrier_email": new_carrier.carrier_email,
            "active_flag": new_carrier.active_flag,
            "carrier_account": {
                # "carrier_account_id": new_carrier_account.carrier_account_id,
                # "carrier_plan": new_carrier_account.carrier_plan,
                "account_name": new_carrier_account.account_name,
                "account_number": new_carrier_account.account_number,
                # "address": new_carrier_account.address,
                "active_flag": new_carrier_account.active_flag,
            },
        }

    except IntegrityError as e:
        logger.error(f"IntegrityError: {str(e)}")
        db.rollback()
        return {"message": "Database error occurred. Please check input data."}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        db.rollback()
        return {"message": f"Error creating carrier: {str(e)}"}


# new for frontend
def update_carrier_service(db: Session, carrier_email: str, carrier_data: dict) -> dict:
    """Business logic for updating a carrier's details based on carrier email."""
    try:
        # Check if the carrier exists based on email
        existing_carrier = check_existing_by_email(db, Carrier, "carrier_email", carrier_email)
        if not existing_carrier:
            raise HTTPException(status_code=404, detail="No carrier found with the given email.")

        # Call CRUD to update the carrier's details
        updated_carrier = update_carrier_crud(db, carrier_email, carrier_data)

        if not updated_carrier:
            raise HTTPException(status_code=500, detail="Error updating carrier details.")

        return {
            "carrier_id": updated_carrier.carrier_id,
            "carrier_name": updated_carrier.carrier_name,
            "carrier_email": updated_carrier.carrier_email,
            "carrier_mobile": updated_carrier.carrier_mobile,
            "carrier_address": updated_carrier.carrier_address,
            "carrier_city": updated_carrier.carrier_city,
            "carrier_state": updated_carrier.carrier_state,
            "carrier_country": updated_carrier.carrier_country,
            "carrier_pincode": updated_carrier.carrier_pincode,
            "carrier_geolocation": updated_carrier.carrier_geolocation,
            "active_flag": updated_carrier.active_flag,
            "remarks": updated_carrier.remarks,
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating carrier: {str(e)}")  

def suspend_or_activate_carrier(db: Session, carrier_email: str, active_flag: int, remarks: str) -> dict:
    """
    Suspend or activate a carrier based on the active_flag input.

    Args:
        db (Session): Database session.
        carrier_email (str): email of the carrier.
        active_flag (int): 1 for activate, 2 for suspend.
        remarks (str): Remarks or notes for the action.

    Returns:
        dict: Updated carrier details or error message.
    """
    try:
        # Validate the active flag value
        if active_flag not in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid active flag value. Use 1 (Activate) or 2 (Suspend)."
            )

        # Check if the carrier exists using utility function
        existing_carrier = check_existing_by_email(db, Carrier, "carrier_email", carrier_email)
        if not existing_carrier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No carrier found with the provided email."
            )

        # Update the carrier's status using the CRUD function
        updated_carrier = suspend_or_activate_carrier_crud(db, carrier_email, active_flag, remarks)

        if not updated_carrier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No carrier found with the provided email."
            )

        # Return the updated carrier details in the correct format
        return {
            "carrier_id": updated_carrier.carrier_id,
            "carrier_name": updated_carrier.carrier_name,
            "carrier_email": updated_carrier.carrier_email,
            "carrier_mobile": updated_carrier.carrier_mobile,
            "remarks": updated_carrier.remarks,
            "active_flag": updated_carrier.active_flag
        }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating carrier status: {str(e)}"
        )



def get_carrier_profile_service(db: Session, carrier_email: str) -> dict:
    """
    Retrieve the profile of a carrier, including account details, based on email.
    """
    try:
        carrier = get_carrier_profile_crud(db, carrier_email)

        if not carrier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrier not found"
            )

        # Ensure carrier.account is a single object
        carrier_account = carrier.account

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
            "remarks": carrier.remarks,
            "account_id": carrier_account.account_id if carrier_account else None,
            "account_name": carrier_account.account_name if carrier_account else None,
            "account_number": carrier_account.account_number if carrier_account else None,
        }

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving carrier profile: {str(e)}"
        )


def get_carriers_profile_list_service(db: Session) -> list:
    """
    Retrieve a list of all carrier profiles, including account details.
    """
    try:
        # Fetch all carriers with account details
        carriers = get_all_carriers_list_crud(db)

        if not carriers:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No carriers found"
            )

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
                "remarks": carrier.remarks,
                "account_id": carrier.account.account_id if carrier.account else None,
                "account_name": carrier.account.account_name if carrier.account else None,
                "account_number": carrier.account.account_number if carrier.account else None,
            }
            for carrier in carriers
        ]

        return carrier_profiles

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving carrier profiles: {str(e)}"
        )