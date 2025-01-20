from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Address Book Models
class AddressBookBase(BaseModel):
    """
    Pydantic model for representing an addressbook.
    """
    customer_id: Optional[int]
    name: str = Field(..., max_length=255)
    address_line_1: str = Field(..., max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., max_length=100)
    state: str = Field(..., max_length=100)
    postal_code: str = Field(..., max_length=20)
    country: str = Field(..., max_length=100)
    mobile: str = Field(..., pattern=r'^\+?\d{10,15}$') # Mobile number validation

class AddressBookCreate(AddressBookBase):
    """
    Pydantic model for receiving input data for creating an address book.
    """
    pass

class AddressBookResponse(AddressBookBase):
    """
    Pydantic model for representing the response data for an address book.
    """
    address_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AddressBookUpdate(BaseModel):
    """
    Pydantic model for receiving input data for updating an address book.
    """
    customer_id: Optional[int] = None
    name: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    mobile: Optional[str] = None

    class Config:
        from_attributes = True
