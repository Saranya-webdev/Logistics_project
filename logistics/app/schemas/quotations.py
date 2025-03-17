from pydantic import BaseModel,root_validator
from datetime import datetime
from typing import List, Optional,Dict
from app.models.enums import PickupMethod, BookingStatus, PackageType,QuotationStatus

# Quotation Models
class Address(BaseModel):
    name: Optional[str] = ""
    mobile: Optional[str] = ""
    email: Optional[str] = ""
    address: Optional[str] = ""
    city: Optional[str] = ""
    stateprovince: Optional[str] = ""
    postal_code: str
    country_code: Optional[str] = ""


class AddressContainer(BaseModel):
    ship_to: Address
    ship_from: Address


class UnitOfMeasurement(BaseModel):
    code: str
    description: str    

class Dimensions(BaseModel):
    unit_of_measurement: UnitOfMeasurement
    length: Optional[str] = None
    width: Optional[str] = None
    height: Optional[str] = None

class PackageWeight(BaseModel):
    unit_of_measurement: UnitOfMeasurement
    weight: float
    
class Packaging(BaseModel):
    code: str
    description: str

class DeliveryTimeInformation(BaseModel):
    package_bill_type: str

class Pickup(BaseModel):
    num_of_pieces: int
    documents_only_indicator: str

class ShippingRate(BaseModel):
    service_code: str
    service_desc: Optional[str] = None
    service_name: str
    transit_time: str
    estimated_arrival_date: str
    estimated_arrival_time: str
    dayofweek: str
    total_charges: float

class PackageDetailsInDb(BaseModel):
    weight: str
    length: str
    width: str
    height: str
    package_type: str
  


class QuotationItemBase(BaseModel):
    packaging: Packaging
    delivery_time_information: DeliveryTimeInformation
    pickup: Pickup
    dimensions: Dimensions
    package_weight: PackageWeight

class ShipmentCreateResponse(BaseModel):
    shipment_id: str
    tracking_number: str
    total_charges: str
    base_service_charge: Optional[str] = None
    residential_surcharge: Optional[str] = None
    label_filename: Optional[str] = None

class QuotationResponse(BaseModel):
    _id: str
    quotation_id: str
    address: AddressContainer
    package_details: List[PackageDetailsInDb]
    status: str
    shipping_rates: List[ShippingRate]
    # from_pincode: Optional[str] = None
    package_count: Optional[int] = None
    pickup_date: Optional[str] = None
    pickup_time: Optional[str] = None
    # to_pincode: Optional[str] = None
    
    class Config:
        populate_by_name = True
        from_attributes = True


class QuotationItemCreate(QuotationItemBase):
    pass

class QuotationItemDetailedResponse(QuotationItemBase):
    item_id: int

    class Config:
        from_attributes = True


class ShippingRateRequest(BaseModel):
    # UserId: str
    # UserType: str
    ship_to_address: Address
    ship_from_address:Address
    package_count: int
    pickup_date: str
    pickup_time:str
    package_details: List[QuotationItemBase]
    status: QuotationStatus = QuotationStatus.unsaved

class ShipmentCreateResponse(BaseModel):
    # status: str
    shipment_id: str
    tracking_number: str
    total_charges: str
    base_service_charge: Optional[str]
    residential_surcharge: Optional[str]  
    label_filename: Optional[str]

class QuotationCreate(BaseModel):
    address: AddressContainer 
    package_details: List[PackageDetailsInDb]
    status: str
    shipping_rates: List[ShippingRate]
    from_pincode: Optional[str] = None
    package_count: Optional[int] = None
    pickup_date: Optional[str] = None
    pickup_time: Optional[str] = None
    to_pincode: Optional[str] = None


class QuotationUpdate(BaseModel):
    customer_id: Optional[int] = None
    created_by: Optional[int] = None
    pickup_method: Optional[PickupMethod] = None
    booking_status: Optional[BookingStatus] = None
    valid_until: Optional[datetime] = None

    class Config:
        from_attributes = True

class QuotationDetailedResponse(ShippingRateRequest):
    quotation_id: int
    quotation_items: List[QuotationItemDetailedResponse]

    class Config:
        from_attributes = True
