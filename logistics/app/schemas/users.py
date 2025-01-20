from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime


# CreateCustomer Model (for receiving input data for creating a customer)
class UserCreate(BaseModel):
    """
    Pydantic model for receiving input data for creating a customer.
    """
    user_name: str
    email: str
    mobile: str
    password: str
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows easy integration with SQLAlchemy 

    # Custom validator for mobile field
    @field_validator('mobile', mode='before') 
    def validate_mobile(cls, value):
        """
        Validate the format of the mobile number.
        """
        if value and (len(value) != 10 or not value.isdigit()):
            raise ValueError("Invalid mobile number format")
        return value

    # Custom validator for email field
    @field_validator('email', mode='before')
    def validate_email(cls, value):
        """
        Validate the format of the email address.
        """
        # Check if the email contains "@" and a valid domain
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Invalid email format")
        return value   

class UpdateUser(BaseModel):
    """
    Pydantic model for receiving input data for updating a user.
    """
    user_name: str
    email: str
    mobile: str
    role: Optional[str] = None

    class Config:
        from_attributes = True        

# class UserWithBookingAndQuotationResponse(BaseModel):
#     """
#     Pydantic model for representing input data for a user with booking and quotation details.
#     """
#     user_id: int
#     user_name: str
#     email: str
#     mobile: str
#     role: Optional[str] = None
#     created_at: datetime
#     updated_at: Optional[datetime] = None
#     # List of bookings
#     bookings: List[BookingDetailedResponse] = [] 
#     # List of quotations
#     quotations: List[QuotationDetailedResponse] = [] 

#     class Config:
#         from_attributes = True
        

class UserResponse(BaseModel):
    user_id: int
    user_name: str
    email: str
    mobile: str
    role: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


