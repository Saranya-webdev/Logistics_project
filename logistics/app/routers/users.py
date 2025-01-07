from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.users import CreateUser, UpdateUser,UserWithBookingAndQuotationResponse, GetAllUsersResponse,QuotationDetailedResponse,BookingDetailedResponse
from app.crud.users import get_user, create_user, update_user, delete_user
from app.database import get_db
from sqlalchemy.exc import IntegrityError
from app.models import Users,Bookings, Quotations
# from app.models import UserPermission

router = APIRouter()

# Create user
@router.post("/createuser/", response_model=CreateUser, status_code=status.HTTP_201_CREATED,
             description="Create a new user and return the created user object.")
async def create_user_api(user: CreateUser, db: Session = Depends(get_db)):

    try:
        # Pass user data to CRUD function
        return create_user(db, user.dict())
    except IntegrityError as e:

        if "UNIQUE constraint failed" in str(e.orig):

            raise HTTPException(status_code=400, detail="User with this email already exists")
        raise HTTPException(status_code=500, detail="Database error occurred")
    
# GET user by ID
@router.get("/{user_id}/viewuser/", response_model=UserWithBookingAndQuotationResponse, status_code=status.HTTP_200_OK)
async def get_user_details(user_id: int, db: Session = Depends(get_db)):
    # Fetch user details
    user = db.query(Users).filter(Users.user_id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
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
def get_all_users_api(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    
    # Convert the SQLAlchemy User instances to Pydantic models
    user_responses = [UserWithBookingAndQuotationResponse.from_orm(user) for user in users]
    
    # Return the response following the GetAllUsersResponse structure
    return {"users": user_responses}

# UPDATE user by ID
@router.put("/{user_id}/updateuser", response_model=UserWithBookingAndQuotationResponse, status_code=status.HTTP_200_OK)
async def edit_user_api(user_id: int, user: UpdateUser, db: Session = Depends(get_db)):
    if not any(value is not None for value in user.dict().values()):
        raise HTTPException(status_code=400, detail="No fields to update")

    updated_user = update_user(db, user_id, user.dict(exclude_unset=True))
    return updated_user

# DELETE user by ID
@router.delete("/{user_id}/deleteuser", status_code=status.HTTP_200_OK)
async def delete_user_api(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(db, user_id)
    return {"detail": f"User {user.username} (ID: {user.user_id}) deleted successfully"}
