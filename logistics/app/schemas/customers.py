from pydantic import BaseModel
from typing import Optional, List
from app.schemas.bookings import BookingDetailedResponse,QuotationDetailedResponse


# Pydantic Schema for Customer Category
class CustomerCategoryBase(BaseModel):
    """
    Pydantic model for representing a customer's category.
    """
    name: str

    class Config:
        from_attributes = True

class CustomerCategoryCreate(CustomerCategoryBase):
    pass

class CustomerCategoryResponse(CustomerCategoryBase):
    id: int

    class Config:
        from_attributes = True

# Pydantic Schema for Customer Type
class CustomerTypeBase(BaseModel):
    name: str

    class Config:
        from_attributes = True

class CustomerTypeCreate(CustomerTypeBase):
    pass

class CustomerTypeResponse(CustomerTypeBase):
    id: int

    class Config:
        from_attributes = True

# Pydantic Schema for Customer
class CustomerBase(BaseModel):
    customer_name: str
    email: str
    mobile: Optional[str]
    company: str
    address: str
    city: str
    state: str
    pincode: Optional[int]
    country: str
    taxid: str
    licensenumber: str
    designation: str
    is_active: bool

    class Config:
        from_attributes = True

class CustomerCreate(CustomerBase):
    """
    Pydantic model for receiving input data for creating a customer.
    """
    category_id: int
    type_id: Optional[int]

class CustomerResponse(CustomerBase):
    customer_id: int
    category: Optional[CustomerCategoryResponse] = None
    customer_type: Optional[CustomerTypeResponse] = None

    class Config:
        from_attributes = True

class CustomerUpdate(CustomerBase):
    category_id: Optional[int]
    type_id: Optional[int]

    class Config:
        from_attributes = True


