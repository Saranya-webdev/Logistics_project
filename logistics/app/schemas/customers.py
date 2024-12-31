from pydantic import BaseModel,field_validator
from typing import Optional
from datetime import datetime
from app.models import CustomerCategory, CustomerType 

# Pydantic Models
class Customer(BaseModel):
    name: str
    email: str
    mobile: Optional[int]
    address: str
    city: str
    state: str
    pincode: Optional[int]
    country: str
    categories: CustomerCategory
    type: CustomerType
    taxid: str
    licensenumber: str
    designation: str
    company: str
    createddate: datetime
    updateddate: datetime

    class Config:
        from_attributes = True


class CustomerResponse(Customer):
    id: int
    createddate: datetime
    updateddate: datetime

    class Config:
        from_attributes = True  # Allows easy integration with SQLAlchemy, so Pydantic can correctly map the database attributes to the response model.

# CreateCustomer Model (for receiving input data for creating a customer)
class CreateCustomer(BaseModel):
    name: str
    email: str
    mobile: Optional[int]
    address: str
    city: str
    state: str
    pincode: Optional[int]
    country: str
    categories: CustomerCategory
    type: CustomerType
    taxid: str
    licensenumber: str
    designation: str
    company: str

    class Config:
        from_attributes = True # Allows easy integration with SQLAlchemy, so Pydantic can correctly map the database attributes to the response model.

    # Custom validator for mobile field
@field_validator('mobile', mode='before') 
def validate_mobile(cls, value):
        if value and (value < 1000000000 or value > 9999999999):
            raise ValueError("Invalid mobile number format")
        return value

# Custom validator for email field
@field_validator('email', mode='before')
def validate_email(cls, value):
    # Check if the email contains "@" and a valid domain
    if "@" not in value or "." not in value.split("@")[-1]:
        raise ValueError("Invalid email format")
    return value

# Custom validator for categories field
@field_validator('categories',  mode='before')
def validate_categories(cls, value):
    if value not in CustomerCategory:
        raise ValueError(f"Invalid category: {value}. Allowed values: {[e.value for e in CustomerCategory]}")
    return value

# Custom validator for type field
@field_validator('type', mode='before')
def validate_type(cls, value):
    if value not in CustomerType:
        raise ValueError(f"Invalid type: {value}. Allowed values: {[e.value for e in CustomerType]}")
    return value
            
