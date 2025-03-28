from pydantic import BaseModel, validator
from datetime import datetime, date, time
from typing import List, Optional, Dict, Any
from app.models.enums import PickupMethod, BookingStatus, PackageType

class BookingSummary(BaseModel):
    booking_id: int
    from_city: str
    from_pincode: str
    to_city: str
    to_pincode: str
    status: str
    action: str

    class ConFig:
        From_attributes = True
            

class BookingItemBase(BaseModel):
    weight: str 
    length: str  
    width: str   
    height: str  
    package_type: str
    # pickup_date: str
    # package_count: int
    

class BookingItemCreate(BookingItemBase):
    pass


class BookingItemDetailedResponse(BaseModel):
    booking_id: int
    item_id: int
    item_weight: float
    item_length: Optional[float] = None
    item_width: Optional[float] = None
    item_height: Optional[float] = None
    package_type: str 
    package_cost: float


    class Config:
        from_attributes = True


class BookingBase(BaseModel):
    from_name: str
    from_mobile: str
    from_email: str
    from_address: str
    from_city: str
    from_state: str
    from_pincode: str
    from_country: str
    to_name: str
    to_mobile: str
    to_email: str
    to_address: str
    to_city: str
    to_state: str
    to_pincode: str
    to_country: str
    carrier_plan: str
    carrier_name: str
    pickup_date: date
    pickup_time: str
    package_count: int
    est_cost: float
    total_cost: float
    est_delivery_date: date
    # booking_date: date
    booking_date: datetime
    booking_status: BookingStatus = BookingStatus.Pending
    tracking_number: Optional[str] = None
    customer_id: int
    class Config:
        use_enum_values = True


class BookingItemList(BaseModel):
    weight: float
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    package_type: str
    package_cost: float
    # volumetric_weight: float


class ShipFromAddress(BaseModel):
    from_name: str
    from_mobile: str
    from_email: str
    from_address: str
    from_city: str
    from_state: str
    from_pincode: str
    from_country: str

class ShipToAddress(BaseModel):
    to_name: str
    to_mobile: str
    to_email: str
    to_address: str
    to_city: str
    to_state: str
    to_pincode: str
    to_country: str


class PackageDetails(BaseModel):
    carrier_plan: str
    carrier_name: str
    service_code: str
    # pickup_date: date
    package_count: int
    est_cost: float
    total_cost: float
    est_delivery_date: date
    booking_date: datetime
    booking_by: str

    @validator("est_delivery_date", "booking_date", pre=True)
    def format_dates(cls, v):
        return v.isoformat() if isinstance(v, date) else v

class BookingCreateRequest(BaseModel):
    customer_id: int
    ship_to_address: ShipToAddress
    ship_from_address: ShipFromAddress
    pickup_date: str
    pickup_time: str
    package_details: PackageDetails
    tracking_number:Optional[str] = None
    booking_items:List[BookingItemList] 

    @validator("pickup_date", pre=True)
    def format_pickup_date(cls, v):
        return v.isoformat() if isinstance(v, date) else v   


class BookingDetailedResponse(BookingBase):
    booking_items: List[BookingItemDetailedResponse]

    class Config:
        from_attributes = True

class BookingListResponse(BaseModel):
    message: str  
    bookings: List[BookingDetailedResponse]
          

class BookingUpdate(BaseModel):
    customer_id: int
    created_by: Optional[int] = None
    # pickup_method: PickupMethod = PickupMethod.user_address
    booking_status: Optional[BookingStatus] = None
    package_type: Optional[PackageType] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    From_address: Optional[str] = None
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

    class ConFig:
        From_attributes = True


class Address(BaseModel):
    Name: Optional[str] = None
    Mobile: Optional[str] = None
    Email: Optional[str] = None
    Address: Optional[str] = None 
    City: Optional[str] = None
    StateProvinceCode: Optional[str] = None
    PostalCode: str 
    CountryCode: Optional[str] = None


class ShippingRateRequest(BaseModel):
    # UserId: str
    # UserType: str
    ship_to_address: Address
    ship_from_address:Address
    package_count: int
    pickup_date: str
    pickup_time:str
    package_details: List[BookingItemBase]
    

class ShippingRateResponse(BaseModel):
    service_code: str
    service_desc: str
    service_name: str
    transit_time: str
    estimated_arrival_date: str
    estimated_arrival_time: str
    dayofweek: str
    total_charges: float
    quotation_id: Optional[str] = None


class ShipmentCreateResponse(BaseModel):
    booking_status: str
    shipment_id: str
    tracking_number: str
    total_charges: str
    base_service_charge: Optional[str]
    residential_surcharge: Optional[str] = None
    label_filename: Optional[str]
    
    