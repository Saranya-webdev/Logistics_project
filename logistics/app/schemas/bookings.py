from pydantic import BaseModel
from datetime import datetime, date, time
from typing import List, Optional
from app.models.enums import PickupMethod, PickupStatus, PackageType,RatingEnum

class BookingSummary(BaseModel):
    booking_id: int
    from_city: str
    from_pincode: str
    to_city: str
    to_pincode: str
    status: str
    action: str

    class Config:
        from_attributes = True
            

# Pydantic Models
class BookingItemBase(BaseModel):
    length: float
    height: float
    weight: float 
    width: float
    package_type: PackageType
    cost: float
    pickup_method: PickupMethod = PickupMethod.user_address
    booking_status: PickupStatus = PickupStatus.pending
    rating: Optional[RatingEnum] = None

    

class BookingItemCreate(BookingItemBase):
    pass

class BookingItemDetailedResponse(BookingItemBase):
    booking_id: int
    item_id: int
    pickup_method: PickupMethod = PickupMethod.user_address

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
    to_name: str
    to_phone_number: str
    to_email: str
    to_address: str
    to_city: str
    to_state: str
    to_country: str
    to_pincode: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    package_count: Optional[int] = None
    estimated_delivery_cost: Optional[float] = None  # Match decimal(10,2)
    estimated_delivery_date: Optional[datetime] = None
    pickup_time: Optional[time] = None
    pickup_date: Optional[date] = None
    rating: Optional[RatingEnum] = None

    

class BookingCreate(BookingBase):
    booking_items: List[BookingItemCreate]

class BookingDetailedResponse(BookingBase):
    booking_id: int
    booking_items: List[BookingItemDetailedResponse]
    payment_status: str  # Can be 'Picked', 'In Transit', 'Delivered', etc.
    rating: Optional[RatingEnum] = None # Rating (1-5)
   

    class Config:
        from_attributes = True

class BookingUpdate(BaseModel):
    customer_id: Optional[int] = None
    created_by: Optional[int] = None
    pickup_method: PickupMethod = PickupMethod.user_address
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

        
