from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


# Address Book Models
class AddressBase(BaseModel):
    address_name: str
    name: str
    mobile: str
    email_id: str
    address: str
    city: str
    state: str
    country: str
    pincode: Optional[str] = None
    company_name: Optional[str] = None
    address_type: str

class AddressBookCreate(AddressBase):
    """
    Pydantic model for receiving input data for creating an address book.
    This can be used for AddressBook insertions.
    """
    city: str
    state: str
    country: str
    postal_code: str
    

class AddressBookResponse(AddressBase):
    """
    Pydantic model for representing the response data for an address book.
    """
    address_id: int

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

class AddressBooksDetailedResponse(AddressBase):
    address_book: List[AddressBookResponse]

    class Config:
        from_attributes = True

class AddressBooksListResponse(BaseModel):
    address_books: List[AddressBookResponse]  
    message: str
