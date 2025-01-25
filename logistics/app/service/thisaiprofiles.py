from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.thisaiprofiles import Associate, AssociatesCredential
from app.utils import check_existing_by_email, process_credentials
import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

def create_associates_service(db: Session, associates_data: dict) -> dict:
    """
    Business logic for creating a associates.
    """
    try:
        # Log validation process
        logger.info("Validating if the associates already exists...")

        # Check if associates already exists using email
        if check_existing_by_email(db, Associate, "associates_email", associates_data["associates_email"]):
            return {"message": "associates already exists"}

        # Ensure all required fields are present (remove remarks from here)
        required_fields = [
            "associates_name", "associates_mobile", "associates_email", "associates_role"
        ]

        missing_fields = [field for field in required_fields if field not in associates_data]

        if missing_fields:
            return {"message": f"Missing required fields: {', '.join(missing_fields)}"}

        # Set default values
        associates_data["active_flag"] = 0  # Default active_flag to 0


        logger.info("Creating new associates...")
        # Create the new associates
        new_associates = Associate(**associates_data)
        db.add(new_associates)
        db.commit()
        db.refresh(new_associates)

        # Return the created associates details
        return {
            "message": "associates created successfully",
            "associates_id": new_associates.associates_id,
            "associates_name": new_associates.associates_name,
            "associates_mobile": new_associates.associates_mobile,
            "associates_email": new_associates.associates_email,
            "associates_role": new_associates.associates_role,
            **{key: getattr(new_associates, key) for key in associates_data.keys()},
        }

    except IntegrityError as e:
        logger.error(f"IntegrityError: {str(e)}")
        db.rollback()
        return {"message": "Database error occurred. Please check input data."}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        db.rollback()
        return {"message": f"Error creating associates: {str(e)}"}

def create_associate_credential_service(db: Session, credentials_data: dict) -> dict:
    try:
        # Log received data to verify correctness
        logger.info(f"Received credentials data: {credentials_data}")
        
        # Ensure that the credentials data is correct
        if not credentials_data.get("email_id") or not credentials_data.get("password"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Both email_id and password are required."
            )

        # Check if associate exists in the database
        associate = db.query(Associate).filter(Associate.associates_email == credentials_data["email_id"]).first()

        if not associate:
            logger.error(f"Associate not found for email: {credentials_data['email_id']}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Associate not found with the provided email."
            )

        # Now proceed with creating associate credential
        new_credential = AssociatesCredential(
            email_id=credentials_data["email_id"],
            password=credentials_data["password"],  # Ensure password is hashed
            associates_id=associate.associates_id
        )

        db.add(new_credential)
        db.commit()
        db.refresh(new_credential)

        logger.info(f"Created associate credential with ID: {new_credential.associates_credential_id}")

        # Return the successful creation response
        return {
            "message": "Associate credential created successfully.",
            "associates_credential": {
                "associates_credential_id": new_credential.associates_credential_id,
                "email_id": new_credential.email_id,
                "associates_id": new_credential.associates_id
            }
        }

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"SQLAlchemy error occurred: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while creating associate credential."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred while creating associate credential."
        )




    

def update_associates_service(db: Session, associates_id: int, associates_data: dict) -> dict:
    """Business logic for updating an associate's details based on associates ID."""
    try:
        # Step 1: Check if the associate exists based on associates_id
        existing_associates = db.query(Associate).filter(Associate.associates_id == associates_id).first()
        if not existing_associates:
            return {"message": "No associates found"}  # Return message if no associate is found

        # Step 2: Update associate details with the provided data
        for field, value in associates_data.items():
            if hasattr(existing_associates, field) and value is not None:
                setattr(existing_associates, field, value)

        # Commit changes to the database
        db.commit()
        db.refresh(existing_associates)

        # Return the updated associate details (including verification_status)
        return {
            "associates_id": existing_associates.associates_id,
            "associates_name": existing_associates.associates_name,
            "associates_email": existing_associates.associates_email,
            "associates_mobile": existing_associates.associates_mobile,
            "associates_role": existing_associates.associates_role,
            "active_flag": existing_associates.active_flag,
            "remarks": existing_associates.remarks,
            "verification_status": existing_associates.verification_status  # Make sure this is included
        }

    except IntegrityError as e:
        db.rollback()
        return {"message": f"Database error: {str(e)}"}
    except Exception as e:
        db.rollback()
        return {"message": f"Error updating associates: {str(e)}"}



def suspend_or_activate_associates(db: Session, associates_mobile: str, active_flag: int, remarks: str) -> dict:
    """
    Suspend or activate a associates based on the active_flag input.

    Args:
        db (Session): Database session.
        associates_mobile (str): Mobile number of the associates.
        active_flag (int): 1 for activate, 2 for suspend.
        remarks (str): Remarks or notes for the action.

    Returns:
        dict: Updated associates details or error message.
    """
    from app.crud.thisaiprofiles import get_associates_by_mobile, update_associates_status
    try:
        # Fetch the associates by mobile
        existing_associates = get_associates_by_mobile(db, associates_mobile)
        if not existing_associates:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No associates found with the provided mobile number."
            )

        # Update the associates's active_flag and remarks
        update_associates_status(db, existing_associates, active_flag, remarks)
        db.refresh(existing_associates)

        # Return the updated associates details
        return {
            'message': 'associates status updated successfully.',
            "associates": {
                "associates_id": existing_associates.associates_id,
                "associates_name": existing_associates.associates_name,
                "associates_email": existing_associates.associates_email,
                "associates_mobile": existing_associates.associates_mobile,
                "associates_role": existing_associates.associates_role,
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
            detail=f"Error updating associates status: {str(e)}"
        )

def verify_associates_service(db: Session, associates_mobile: str, verification_status: str) -> dict:
    """
    Verify the associates and update their verification status and active flag.

    Args:
        db (Session): Database session.
        associates_mobile (str): Mobile number of the associate.
        verification_status (str): Verification status ('Verified' or 'Not Verified').

    Returns:
        dict: Updated associate details or error message.
    """
    try:
        # Step 1: Retrieve the associate based on the mobile number
        existing_associates = db.query(Associate).filter(Associate.associates_mobile == associates_mobile).first()

        if not existing_associates:
            # Step 2: Return message if the associate is not found
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No associate found with the provided mobile number."
            )

        # Step 3: Update verification status and active flag based on the verification status
        if verification_status.lower() == "verified":
            existing_associates.verification_status = "Verified"
            existing_associates.active_flag = 1  # Set active flag to 1 if verified
        else:
            existing_associates.verification_status = verification_status
            # Optionally, you can set active_flag to 0 if verification status is not "Verified"
            existing_associates.active_flag = 0

        # Commit the changes to the database
        db.commit()
        db.refresh(existing_associates)

        # Step 4: Return the updated associate details
        return {
            "message": "Associate verification status updated successfully.",
            "associate": {
                "associates_id": existing_associates.associates_id,
                "associates_name": existing_associates.associates_name,
                "associates_email": existing_associates.associates_email,
                "associates_mobile": existing_associates.associates_mobile,
                "verification_status": existing_associates.verification_status,
                "active_flag": existing_associates.active_flag,
            },
        }
    except Exception as e:
        # Rollback the transaction in case of an unexpected error
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying associate: {str(e)}"
        )

    

def get_associates_profile(db: Session, associates_mobile: str) -> dict:
    """Retrieve the profile of an associate based on their mobile number."""
    from app.crud.thisaiprofiles import get_associates_by_mobile
    
    # Retrieve the associate by mobile
    associates = get_associates_by_mobile(db, associates_mobile)
    
    # Handle case when associates is None
    if associates is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Associate with mobile number {associates_mobile} not found"
        )
    
    # Return the associate profile details if found
    return {
        "associates_id": associates.associates_id,
        "associates_name": associates.associates_name,
        "associates_email": associates.associates_email,
        "associates_mobile": associates.associates_mobile,
        "associates_role": associates.associates_role,
        "active_flag": associates.active_flag,
        "remarks": associates.remarks
    }


def get_associatess_profile_list(db: Session) -> list:
    """Retrieve a list of all associates profiles."""
    try:
        # Get the list of all associatess from the database without filters
        associatess = db.query(Associate).all()  # This will retrieve all associatess
        
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
            for associates in associatess
        ]
        return associates_profiles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving associates profiles: {str(e)}"
        )


def soft_delete_associates_service(db: Session, associates_id: int):
    """Service layer function to soft delete a associates."""
    from app.crud.thisaiprofiles import soft_delete_associates_crud
    try:
        # Call the CRUD function to soft delete the associates
        deleted_associates = soft_delete_associates_crud(db, associates_id)
        return deleted_associates
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while trying to soft delete the associates: {str(e)}"
        )