from app.models.users import Users
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.crud.users import get_user, create_user, update_user
from app.utils import log_and_raise_exception,check_duplicate_email_or_mobile
import logging
from sqlalchemy.orm import Session

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def create_user_service(db, user_data: dict):
    """
    Business logic for creating a new user.
    Checks if email or mobile number already exists in the database.
    """
    try:
        existing_user = check_duplicate_email_or_mobile(db, Users, user_data['email'], user_data['mobile'])
        if existing_user:
            details = []
            if existing_user.email == user_data['email']:
                details.append(f"Email {user_data['email']} already exists.")
            if existing_user.mobile == user_data['mobile']:
                details.append(f"Mobile number {user_data['mobile']} already exists.")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" ".join(details))
        return create_user(db, user_data)
    except IntegrityError as e:
        db.rollback()
        log_and_raise_exception(f"Error creating user: {str(e)}", status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error creating user: {str(e)}", 500)
    
def update_user_service(db, user_id: int, user_data: dict):
    """
    Business logic for updating user details.
    """
    user = get_user(db, user_id)
    if not user:
        logger.error(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    try:
        # Update each attribute of the user
        for key, value in user_data.items():
            setattr(user, key, value)
        
        # Commit changes to the database
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        # Rollback on error and raise HTTP Exception
        db.rollback()
        log_and_raise_exception(f"Error updating user: {str(e)}", status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Rollback on any other error
        db.rollback()
        log_and_raise_exception(f"Error updating user with ID {user_id}: {str(e)}", 500)

