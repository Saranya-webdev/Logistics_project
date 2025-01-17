from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session,joinedload
from app.crud.users import get_user, create_user, update_user, delete_user
from app.databases.mysqldb import get_db
from sqlalchemy.exc import IntegrityError
from app.models import Users
from app.schemas.users import UserCreate, UpdateUser, UserResponse
from app.service.users import create_user, update_user
from typing import List
import logging

router = APIRouter()

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create user
@router.post("/createuser/", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
             description="Create a new user and return the created user object.")
async def create_user_api(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user and return the created user object.
    """
    try:
        return create_user(db, user.dict())
    except IntegrityError as e:
        logger.error(f"Integrity error while creating user: {str(e)}")
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(status_code=400, detail="User with this email already exists")
        raise HTTPException(status_code=500, detail="Database error occurred")
    
# GET user by ID
@router.get("/{user_id}/viewuser/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def single_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single user by ID.
    """
    user = get_user(db, user_id)
    if user is None:
        logger.error(f"User ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User ID not found")
    
    # Creating the response object with all required fields
    response = UserResponse(
        user_id=user.user_id,
        user_name=user.user_name,  # Adjust according to your actual field name
        email=user.email,
        mobile=user.mobile,
        role=user.role,  # Optional, provide if available
        created_at=user.created_at,
        updated_at=user.updated_at
    )
    
    return response


# GET all users
@router.get("/allusers", response_model= List[UserResponse])
def get_all_users_api(db: Session = Depends(get_db)):
    """
    Retrieve all customers.
    """
    users = db.query(Users).all()
    return users

# UPDATE user by ID
@router.put("/{user_id}/updateuser", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def edit_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db)):
    """
    Update user information by ID.
    """
    if not any(value is not None for value in user.dict().values()):
        raise HTTPException(status_code=400, detail="No fields to update")
    updated_user = update_user(db, user_id, user.dict(exclude_unset=True))
    return UserResponse.from_orm(updated_user)

# DELETE user by ID
@router.delete("/{user_id}/deleteuser", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a customer by ID.
    """
    user = get_user(db, Users, user_id)
    if not user:
        logger.error(f"User ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(db, user_id)
    return {"detail": f"User {user.user_name} (ID: {user.user_id}) deleted successfully"}
