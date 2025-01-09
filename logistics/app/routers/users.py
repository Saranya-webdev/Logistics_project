from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session,joinedload
from app.crud.users import get_user, create_user, update_user, delete_user
from app.databases.mysqldb import get_db
from sqlalchemy.exc import IntegrityError
from app.models import Users,Bookings, Quotations
from app.utils import validate_entry_by_id
from app.schemas.users import (CreateUser, UpdateUser, UserWithBookingAndQuotationResponse, 
GetAllUsersResponse, QuotationDetailedResponse, BookingDetailedResponse)
import logging

router = APIRouter()

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create user
@router.post("/createuser/", response_model=CreateUser, status_code=status.HTTP_201_CREATED,
             description="Create a new user and return the created user object.")
async def create_user_api(user: CreateUser, db: Session = Depends(get_db)):
    """
    Create a new user and return the created user object.
    """
    try:
        new_user = create_user(db, user.dict())
        return CreateUser.from_orm(new_user)
    except IntegrityError as e:
        logger.error(f"Integrity error while creating user: {str(e)}")
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(status_code=400, detail="User with this email already exists")
        raise HTTPException(status_code=500, detail="Database error occurred")
    
# GET user by ID
@router.get("/{user_id}/viewuser/", response_model=UserWithBookingAndQuotationResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single user by ID.
    """
    # Fetch user details
    validate_entry_by_id(user_id, db, Users, "User")  # Validate User ID
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        logger.error(f"User ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User ID not found")
    bookings = db.query(Bookings).filter(Bookings.user_id == user_id).all()
    quotations = db.query(Quotations).filter(Quotations.user_id == user_id).all()
    return UserWithBookingAndQuotationResponse(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        mobile=user.mobile,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at,
        bookings=[BookingDetailedResponse.from_orm(booking) for booking in bookings],
        quotations=[QuotationDetailedResponse.from_orm(quotation) for quotation in quotations]
    )  

# GET all users
@router.get("/allusers", response_model=GetAllUsersResponse)
def get_all_users(db: Session = Depends(get_db)):
    """
    Retrieve all customers.
    """
    users = db.query(Users).options(joinedload(Users.bookings), joinedload(Users.quotations)).all()
    
    # Convert the SQLAlchemy User instances to Pydantic models
    user_responses = [UserWithBookingAndQuotationResponse.from_orm(user) for user in users]
    
    # Return the response following the GetAllUsersResponse structure
    return GetAllUsersResponse(users=user_responses)

# UPDATE user by ID
@router.put("/{user_id}/updateuser", response_model=UserWithBookingAndQuotationResponse, status_code=status.HTTP_200_OK)
async def edit_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db)):
    """
    Update user information by ID.
    """
    if not any(value is not None for value in user.dict().values()):
        raise HTTPException(status_code=400, detail="No fields to update")
    updated_user = update_user(db, user_id, user.dict(exclude_unset=True))
    return UserWithBookingAndQuotationResponse.from_orm(updated_user)

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
    return {"detail": f"User {user.username} (ID: {user.user_id}) deleted successfully"}
