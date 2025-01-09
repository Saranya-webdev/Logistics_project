from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime
from app.models.customers import CustomerCategory, CustomerType 
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas.bookings import BookingDetailedResponse

# Pydantic Models
class Customer(BaseModel):
    """
    Pydantic model for representing a Customer.
    """
    name: str
    email: str
    mobile: str
    address: str
    city: str
    state: str
    pincode: Optional[int]
    country: str
    category_id: int
    type_id: Optional[int]  # Updated to match the database model
    taxid: str
    licensenumber: str
    designation: str
    company: str
    createddate: datetime
    updateddate: datetime

    class Config:
        from_attributes = True


class CustomerResponse(Customer):
    """
    Pydantic model for representing the response of a Customer.
    """
    customer_id: int
    bookings: List[BookingDetailedResponse]

    class Config:
        from_attributes = True


# CreateCustomer Model (for receiving input data for creating a customer)
class CreateCustomer(BaseModel):
    """
    Pydantic model for receiving input data for creating a customer.
    """
    name: str
    email: str
    mobile: Optional[str]
    address: str
    city: str
    state: str
    pincode: Optional[int]
    country: str
    category_id: int
    type_id: int
    taxid: str
    licensenumber: str
    designation: str
    company: str

    class Config:
        from_attributes = True  # Allows easy integration with SQLAlchemy

    # Custom validator for mobile field
    @field_validator('mobile', mode='before')
    def validate_mobile(cls, value):
        """
        Validate the format of the mobile number.
        """
        if value and (value < 1000000000 or value > 9999999999):
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


class UpdateCustomer(BaseModel):
    """
    Pydantic model for receiving input data for updating a customer.
    """
    name: Optional[str]
    email: Optional[str]
    mobile: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pincode: Optional[int]
    country: Optional[str]
    category_id: Optional[int]
    type_id: Optional[int]
    taxid: Optional[str]
    licensenumber: Optional[str]
    designation: Optional[str]
    company: Optional[str]

    class Config:
        from_attributes = True