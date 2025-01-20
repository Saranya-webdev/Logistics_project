from pydantic import BaseModel
from typing import Optional, List


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

class CustomerListResponse(BaseModel):
    customer_name: str
    mobile: Optional[str]
    email: str

    class Config:
        from_attributes = True    

# Response model for detailed customer information
class CustomerDetailedResponse(BaseModel):
    customer_name: str
    mobile: Optional[str]
    email: str
    address: str
    city: str
    state: str
    country: str
    pincode: Optional[int]

    class Config:
        from_attributes = True            

class CustomerUpdate(CustomerBase):
    category_id: Optional[int]
    type_id: Optional[int]

    class Config:
        from_attributes = True


# Response model for a booking list item
class BookingListItem(BaseModel):
    from_city: str
    from_pincode: Optional[int]
    to_city: str
    to_pincode: Optional[int]
    type: str
    status: str
    action: str

    class Config:
        from_attributes = True

# Response model for customer's booking list
class CustomerBookingListResponse(BaseModel):
    customer_name: str
    bookings: List[BookingListItem]

    class Config:
        from_attributes = True


# Response model for detailed booking information
class CustomerBookingDetailedResponse(BaseModel):
    name: str
    from_address: str
    to_address: str
    length: float
    height: float
    weight: float
    width: float
    package_type: str
    cost: float
    delivery_date: str
    num_packages: int

    class Config:
        from_attributes = True        