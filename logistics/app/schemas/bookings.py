from pydantic import BaseModel
from datetime import datetime,date,time
from typing import List, Optional
from app.models import PickupMethod, PickupStatus,PackageType  # Importing the Enums


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
    item_id: int
    # length: float
    # width: float
    # height: float
    # weight: float
    # package_type: PackageTye
    # cost: float
    

    class Config:
        from_attributes = True


class BookingBase(BaseModel):
    booking_id: int
    user_id: int
    created_by: int
    name: str
    phone_number: str
    email: str
    address: str
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

    created_at: datetime
    updated_at: datetime

    estimated_delivery_date: Optional[datetime] = None
    estimated_delivery_cost: Optional[int] = None

    pickup_time: Optional[time] = None
    pickup_date: Optional[date] = None




class BookingCreate(BookingBase):
    booking_items: List[BookingItemCreate]


class BookingDetailedResponse(BookingBase):
    from_address: Optional[str] = None
    to_address: str
    package_type: Optional[PackageType] = None
    booking_status: PickupStatus = PickupStatus.pending
    booking_items: List[BookingItemDetailedResponse]
    pickup_date: Optional[date] = None
    pickup_time: Optional[time] = None

    class Config:
        from_attributes = True

class BookingUpdate(BaseModel):
    booking_id: int
    user_id: Optional[int] = None
    created_by: Optional[int] = None
    pickup_method: Optional[PickupMethod] = None
    booking_status: Optional[PickupStatus] = None
    package_type: Optional[PackageType] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
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
    # length: float
    # width: float
    # height: float
    # weight: float
    # package_type: PackageTye
    # cost: float

    class Config:
        from_attributes = True


class QuotationBase(BaseModel):
    quotation_id: int
    user_id: int
    created_by: int
    pickup_method: PickupMethod
    bookin_status: PickupStatus = PickupStatus.pending
    valid_until: datetime
    created_at: datetime
    updated_at: datetime


class QuotationCreate(QuotationBase):
    quotation_items: List[QuotationItemCreate]


class QuotationDetailedResponse(QuotationBase):
    quotation_id: int
    quotation_items: List[QuotationItemDetailedResponse]
    valid_until: datetime
    updated_at: datetime 

    class Config:
        from_attributes = True

class QuotationUpdate(BaseModel):
    user_id: Optional[int] = None
    created_by: Optional[int] = None
    pickup_method: Optional[PickupMethod] = None
    booking_status: Optional[PickupStatus] = None
    valid_until: Optional[datetime] = None

    class Config:
        from_attributes = True        


class AddressBookBase(BaseModel):
    user_id: int
    name: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state: str
    postal_code: str
    country: str
    mobile: str


class AddressBookCreate(AddressBookBase):
    pass


class AddressBookResponse(AddressBookBase):
    address_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AddressBookUpdate(BaseModel):
    user_id: Optional[int] = None
    name: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    mobile: Optional[str] = None
    # Add any other fields that can be updated in the AddressBook model

    class Config:
        from_attributes = True        
