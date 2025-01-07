from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime
# from app.models import UserPermission
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.bookings import BookingDetailedResponse,QuotationDetailedResponse

# Pydantic Models
class User(BaseModel):
    username: str
    email: str
    mobile: str
    address: str
    city: str
    state: str
    pincode: Optional[int]
    country: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CreateUser(BaseModel):
    username: str
    email: str
    mobile: str
    password: str
    # permission_id: int
    role: str
    created_at: datetime
    updated_at: datetime
    


    class Config:
        from_attributes = True  # Allows easy integration with SQLAlchemy 

    # Custom validator for mobile field
@field_validator('mobile', mode='before') 
def validate_mobile(cls, value):
    if not value.isdigit():  # Ensure the value is numeric
        raise ValueError("Mobile number must contain only digits")
    
    value = int(value)  # Convert the string to an integer
    if value < 1000000000 or value > 9999999999:  # Validate the range
        raise ValueError("Invalid mobile number format")
    return value

    # Custom validator for email field
@field_validator('email', mode='before')
def validate_email(cls, value):
        # Check if the email contains "@" and a valid domain
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Invalid email format")
        return value   
        
class UpdateUser(BaseModel):
    username: str
    email: str
    mobile: str
    role:Optional[str] = None
    

    class Config:
        from_attributes = True        


class UserWithBookingAndQuotationResponse(BaseModel):
    user_id: int
    username: str
    email: str
    mobile: str
    role: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    bookings: List[BookingDetailedResponse] = []  # List of bookings
    quotations: List[QuotationDetailedResponse] = []  # List of quotations

    class Config:
        from_attributes = True

class GetAllUsersResponse(BaseModel):
    users: List[UserWithBookingAndQuotationResponse]

    class Config:
        from_attributes = True

class GetUserResponse(BaseModel):
    user: UserWithBookingAndQuotationResponse

    class Config:
        from_attributes = True

