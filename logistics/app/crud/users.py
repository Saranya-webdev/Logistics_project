from sqlalchemy.orm import Session, joinedload
from app.models import Users
from fastapi import HTTPException
# from app.models import UserPermission
from passlib.hash import bcrypt
from app.schemas.users import UserWithBookingAndQuotationResponse

# Reusable function to populate dynamic entries (categories, customer types, etc.)
def populate_dynamic_entries(db: Session, model, entries: list):
    for entry in entries:
        if not db.query(model).filter(model.name == entry).first():
            db.add(model(name=entry))
    db.commit()


# Fetches all customers from the database.
def get_all_users(db):
    users = db.query(Users).all()
    return users

# Fetches a customer by ID.
def get_user(db: Session, user_id: int):
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user  

# Creates a new customer in the database.
def create_user(db: Session, user_data: dict):
    # Validate required fields
    required_fields = ["username", "password", "email", "mobile", "role"]
    for field in required_fields:
        if field not in user_data:
            raise HTTPException(status_code=400, detail=f"{field} is required")

    # Hash the password
    plain_password = user_data.get("password")
    hashed_password = bcrypt.hash(plain_password)

    # Map fields to the User model
    new_user_data = {
        "username": user_data["username"],
        "password_hash": hashed_password,
        "email": user_data["email"],
        "mobile": user_data["mobile"],
        "role": user_data.get("role", "default_role"),
        "created_at": user_data.get("created_at")
    }

    # Create and add the new user to the database
    new_user = Users(**new_user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return the Pydantic response model
    return UserWithBookingAndQuotationResponse.from_orm(new_user)

# Updates a customer by ID.
def update_user(db: Session, user_id: int, user_data: dict):
    existing_user = db.query(Users).filter(Users.user_id == user_id).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User ID not found")
    
    # Update fields dynamically
    for key, value in user_data.items():
        setattr(existing_user, key, value)

    db.commit()
    db.refresh(existing_user)
    
    # Return updated user in Pydantic model format
    return UserWithBookingAndQuotationResponse.from_orm(existing_user)

# Deletes a customer by ID.
def delete_user(db: Session, user_id: int):
    user_to_delete = db.query(Users).filter(Users.user_id == user_id).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user_to_delete)
    db.commit()
    return {"detail": f"User {user_to_delete.username} (ID: {user_to_delete.user_id}) deleted successfully"}
  