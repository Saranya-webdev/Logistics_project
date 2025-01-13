from pydantic import BaseModel
from datetime import datetime,date,time
from typing import List, Optional
from app.models.bookings import PickupMethod, PickupStatus,PackageType 

# Pydantic Models
class BookingItemBase(BaseModel):
    """
    Pydantic model for representing a Booking Item.
    """
    weight: float
    length: float
    width: float
    height: float
    package_type: PackageType
    cost: float


class BookingItemCreate(BookingItemBase):
    """
    Pydantic model of input data for creating a Booking Item.
    """
    pass


class BookingItemDetailedResponse(BookingItemBase):
    """
    Pydantic model for receiving and responding with Booking Item Details.
    """
    booking_id: int
    item_id: int

    class Config:
        from_attributes = True


class BookingBase(BaseModel):
    """
    Pydantic model for representing a booking.
    """
    user_id: int
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
    pickup_time: Optional[time] = None
    pickup_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime


class BookingCreate(BookingBase):
    """
    Pydantic model for creating a Booking.
    """
    booking_items: List[BookingItemCreate]


class BookingDetailedResponse(BookingBase):
    """
    Pydantic model for receiving the details of a booking.
    """
    booking_id: int
    booking_items: List[BookingItemDetailedResponse]
    pickup_date: Optional[date] = None
    pickup_time: Optional[time] = None

    class Config:
        from_attributes = True

class BookingUpdate(BaseModel):
    """
    Pydantic model for receiving input data for updating a booking.
    """
    # booking_id: int
    user_id: Optional[int] = None
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
    to_phone_number: Optional[int] = None
    to_email: Optional[str] = None
    to_address: Optional[str] = None
    to_city: Optional[str] = None
    to_state: Optional[str] = None
    to_country: Optional[str] = None
    to_pincode: Optional[int] = None
    estimated_delivery_date: Optional[datetime] = None
    estimated_delivery_cost: Optional[int] = None
    pickup_time: Optional[time] = None
    pickup_date: Optional[date] = None
    booking_items: Optional[List[BookingItemCreate]] = None  # Allow updating booking items

    class Config:
        from_attributes = True        


# Quotation Models 
class QuotationItemBase(BaseModel):
    """
    Pydantic model for representing a quotation  item.
    """
    weight: float
    length: float
    width: float
    height: float
    package_type: PackageType
    cost: float


class QuotationItemCreate(QuotationItemBase):
    """
    Pydantic model for receiving input data for creating a quotation item.
    """
    pass


class QuotationItemDetailedResponse(QuotationItemBase):
    """
    Pydantic model for receiving and responding with quotation item details.
    """
    item_id: int

    class Config:
        from_attributes = True


class QuotationBase(BaseModel):
    """
    Pydantic model for representing a quotation.
    """
    user_id: int
    created_by: int
    pickup_method: PickupMethod
    bookin_status: PickupStatus = PickupStatus.pending
    valid_until: datetime
    created_at: datetime
    updated_at: datetime


class QuotationCreate(QuotationBase):
    """
    Pydantic model for receiving input data for creating a quotation.
    """
    quotation_items: List[QuotationItemCreate]


class QuotationDetailedResponse(QuotationBase):
    """
    Pydantic model for representing quotation details.
    """
    quotation_id: int
    quotation_items: List[QuotationItemDetailedResponse]

    class Config:
        from_attributes = True

class QuotationUpdate(BaseModel):
    """
    Pydantic model for receiving input data for updating a quotation.
    """
    user_id: Optional[int] = None
    created_by: Optional[int] = None
    pickup_method: Optional[PickupMethod] = None
    booking_status: Optional[PickupStatus] = None
    valid_until: Optional[datetime] = None

    class Config:
        from_attributes = True        


# Address Book Models
class AddressBookBase(BaseModel):
    """
    Pydantic model for representing an addressbook.
    """
    user_id:  Optional[int]
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
    user_id: Optional[int] = None
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


class UserOrCustomerWithBookingsResponse(BaseModel):
    booking_id: int
    name: str
    email: str
    phone_number: str
    created_at: datetime
    bookings: List[BookingDetailedResponse]

    class Config:
        from_attributes = True
