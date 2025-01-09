from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models import Users
from passlib.hash import bcrypt
from app.schemas.users import UserWithBookingAndQuotationResponse
import logging

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Reusable function to populate dynamic entries (categories, customer types, etc.)
def populate_dynamic_entries(db: Session, model, entries: list):
    for entry in entries:
        if not db.query(model).filter(model.name == entry).first():
            db.add(model(name=entry))
    db.commit()

# Fetches all customers from the database.
def get_all_users(db: Session):
    """
    Retrieve all users from the database with their booking details.
    """
    try:
        return db.query(Users).options(joinedload(Users.bookings)).all()
    except Exception as e:
        logger.error(f"Error fetching all users: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching all users")

# Fetches a customer by ID.
def get_user(db: Session, user_id: int):
    """
    Retrieve a user by their ID.
    """
    try:
       user = db.query(Users).filter(Users.user_id == user_id).first()
       if not user:
          raise HTTPException(status_code=404, detail="User not found")
       return user 
    except Exception as e:
        logger.error(f"Error fetching user with ID {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching user")
 

# Creates a new customer in the database.
def create_user(db: Session, user_data: dict):
    # Validate required fields
    """
    Create a new user in the database.
    """
    try:
       required_fields = ["username", "password", "email", "mobile", "role"]
       for field in required_fields:
        if field not in user_data:
            raise HTTPException(status_code=400, detail=f"{field} is required")

        # Hash the password
        hashed_password = bcrypt.hash(user_data["password"])

        # Map fields to the User model
        new_user_data = {
        "username": user_data["username"],
        "password_hash": hashed_password,
        "email": user_data["email"],
        "mobile": user_data["mobile"],
        "role": user_data.get("role", "default_role"),
        "created_at": user_data.get("created_at")}

        # Create and add the new user to the database
        db_user = Users(**new_user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        # Return the Pydantic response model
        return UserWithBookingAndQuotationResponse.from_orm(db_user)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user: {str(e)}")    
        raise HTTPException(status_code=500, detail="Error creating user")

# Updates a customer by ID.
def update_user(db: Session, user_id: int, user_data: dict):
    """
    Update an existing customer by their ID.
    """
    try:
       existing_user = db.query(Users).filter(Users.user_id == user_id).first()
       if not existing_user:
        raise HTTPException(status_code=404, detail="User ID not found")
    
       # Update fields dynamically
       for key, value in user_data.items():
        setattr(existing_user, key, value)

       db.commit()
       db.refresh(existing_user)
       return UserWithBookingAndQuotationResponse.from_orm(existing_user)
    except Exception as e:
       db.rollback()
       logger.error(f"Error updating user with ID {user_id}: {str(e)}")
       raise HTTPException(status_code=500, detail="Error updating user")

# Deletes a customer by ID.
def delete_user(db: Session, user_id: int):
    """
    Delete a customer by their ID.
    """
    try:
       user_to_delete = db.query(Users).filter(Users.user_id == user_id).first()
       if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    
       db.delete(user_to_delete)
       db.commit()
       return {"detail": f"User {user_to_delete.username} (ID: {user_to_delete.user_id}) deleted successfully"}
    except Exception as e:
       db.rollback()
       logger.error(f"Error deleting user with ID {user_id}: {str(e)}")
       raise HTTPException(status_code=500, detail="Error deleting user")
  