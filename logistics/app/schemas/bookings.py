from pydantic import BaseModel
from datetime import datetime, date, time
from typing import List, Optional
from app.models.bookings import PickupMethod, PickupStatus, PackageType

# Pydantic Models
class BookingItemBase(BaseModel):
    weight: float
    length: float
    width: float
    height: float
    package_type: PackageType
    cost: float

class BookingItemCreate(BookingItemBase):
    pass

class BookingItemDetailedResponse(BookingItemBase):
    booking_id: int
    item_id: int

    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    customer_id: int
    created_by: int
    name: str
    phone_number: str
    email: str
    from_address: str
    city: str
    state: str
    country: str
    pincode: Optional[int] = None
    pickup_method: PickupMethod
    booking_status: PickupStatus = PickupStatus.pending
    to_name: str
    to_phone_number: str
    to_email: str
    to_address: str
    to_city: str
    to_state: str
    to_country: str
    to_pincode: Optional[int] = None
    estimated_delivery_date: Optional[datetime] = None
    estimated_delivery_cost: Optional[int] = None
    package_count: Optional[int] = None
    pickup_time: Optional[time] = None
    pickup_date: Optional[date] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class BookingCreate(BookingBase):
    booking_items: List[BookingItemCreate]

class BookingDetailedResponse(BookingBase):
    booking_id: int
    booking_items: List[BookingItemDetailedResponse]

    class Config:
        from_attributes = True

class BookingUpdate(BaseModel):
    customer_id: Optional[int] = None
    created_by: Optional[int] = None
    pickup_method: Optional[PickupMethod] = None
    booking_status: Optional[PickupStatus] = None
    package_type: Optional[PackageType] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    from_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[int] = None
    to_name: Optional[str] = None
    to_phone_number: Optional[str] = None
    to_email: Optional[str] = None
    to_address: Optional[str] = None
    to_city: Optional[str] = None
    to_state: Optional[str] = None
    to_country: Optional[str] = None
    to_pincode: Optional[int] = None
    estimated_delivery_date: Optional[datetime] = None
    estimated_delivery_cost: Optional[int] = None
    package_count: int
    pickup_time: Optional[time] = None
    pickup_date: Optional[date] = None
    booking_items: Optional[List[BookingItemCreate]] = None

    class Config:
        from_attributes = True

# Quotation Models
class QuotationItemBase(BaseModel):
    weight: float
    length: float
    width: float
    height: float
    package_type: PackageType
    cost: float

class QuotationItemCreate(QuotationItemBase):
    pass

class QuotationItemDetailedResponse(QuotationItemBase):
    item_id: int

    class Config:
        from_attributes = True

class QuotationBase(BaseModel):
    customer_id: int
    created_by: int
    pickup_method: PickupMethod
    booking_status: PickupStatus = PickupStatus.pending
    valid_until: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class QuotationCreate(QuotationBase):
    quotation_items: List[QuotationItemCreate]

class QuotationUpdate(BaseModel):
    customer_id: Optional[int] = None  # Fix typo here
    created_by: Optional[int] = None
    pickup_method: Optional[PickupMethod] = None
    booking_status: Optional[PickupStatus] = None
    valid_until: Optional[datetime] = None

    class Config:
        from_attributes = True

class QuotationDetailedResponse(QuotationBase):
    quotation_id: int
    quotation_items: List[QuotationItemDetailedResponse]

    class Config:
        from_attributes = True

     
# Address Book Models
class AddressBookBase(BaseModel):
    """
    Pydantic model for representing an addressbook.
    """
    customer_id:  Optional[int]
    name: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state: str
    postal_code: str
    country: str
    mobile: str


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



