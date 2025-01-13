from sqlalchemy.orm import Session, joinedload
from app.models.users import Users
from app.utils import log_and_raise_exception,get_entity_by_id
from passlib.hash import bcrypt
from app.schemas.users import UserResponse


# Fetches all customers from the database.
def get_all_users(db: Session):
    """
    Retrieve all users from the database .
    """
    try:
        return db.query(Users).all()
    except Exception as e:
        log_and_raise_exception(f"Error fetching all users: {str(e)}", 500)

# Fetches a customer by ID.
def get_user(db: Session, user_id: int):
    """
    Retrieve a user by their ID.
    """
    return get_entity_by_id(db, Users, user_id, 'user_id')
 
# Creates a new user in the database.
def create_user(db: Session, user_data: dict):
    """
    Create a new user in the database.
    """
    try:
        # Validate required fields
        required_fields = ["user_name", "password", "email", "mobile", "role"]
        for field in required_fields:
            if field not in user_data:
                log_and_raise_exception(f"{field} is required", 400)

        # Hash the password
        hashed_password = bcrypt.hash(user_data["password"])

        # Map fields to the User model
        new_user_data = {
            "user_name": user_data["user_name"],
            "password_hash": hashed_password,
            "email": user_data["email"],
            "mobile": user_data["mobile"],
            "role": user_data.get("role", "default_role"),
            "created_at": user_data.get("created_at"),
            "category_id": user_data['category_id'],
            "type_id": user_data['type_id']
        }

        # Create and add the new user to the database
        db_user = Users(**new_user_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Return the Pydantic response model
        return UserResponse.from_orm(db_user)

    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error creating user: {str(e)}", 500)
        

# Updates a customer by ID.
def update_user(db: Session, user_id: int, user_data: dict):
    """
    Update an existing user by their ID.
    """
    existing_user = get_entity_by_id(db, Users, user_id, 'user_id')
    try:
       # Update fields dynamically
       for key, value in user_data.items():
        setattr(existing_user, key, value)

       db.commit()
       db.refresh(existing_user)
       return UserResponse.from_orm(existing_user)
    except Exception as e:
       db.rollback()
       log_and_raise_exception(f"Error updating user with ID {user_id}: {str(e)}" , 500)


# Deletes a customer by ID.
def delete_user(db: Session, user_id: int):
    """
    Delete a user by their ID.
    """
    user_to_delete = get_entity_by_id(db, Users, user_id, 'user_id')
    try:
       db.delete(user_to_delete)
       db.commit()
       return {"detail": f"User {user_to_delete.user_name} (ID: {user_to_delete.user_id}) deleted successfully"}
    except Exception as e:
       db.rollback()
       log_and_raise_exception(f"Error deleting user with ID {user_id}: {str(e)}", 500)
