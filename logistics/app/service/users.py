from app.models.users import Users
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

def check_user_exists(db, user_id: int):
    """
    Check if the user exists by ID.
    """
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} does not exist.")
    return user

def create_user(db, user_data: dict):
    """
    Business logic for creating a new user.
    Checks if email or mobile number already exists in the database.
    """
    # Check if the email already exists
    existing_email = db.query(Users).filter(Users.email == user_data['email']).first()
    
    # Check if the mobile number already exists
    existing_mobile = db.query(Users).filter(Users.mobile == user_data['mobile']).first()

    # If both email and mobile number exist, raise an exception
    if existing_email and existing_mobile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user_data['email']} and mobile number {user_data['mobile']} already exist."
        )
    
    # If only email exists, raise an exception
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user_data['email']} already exists."
        )
    
    # If only mobile exists, raise an exception
    if existing_mobile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with mobile number {user_data['mobile']} already exists."
        )
    
    # Proceed with creating the new user if neither email nor mobile number exists
    try:
        new_user = Users(**user_data)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        db.rollback()  # Rollback the transaction in case of an integrity error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating user: {str(e)}")
    
def update_user(db, user_id: int, user_data: dict):
    """
    Business logic for updating user details.
    """
    user = check_user_exists(db, user_id)
    for key, value in user_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
