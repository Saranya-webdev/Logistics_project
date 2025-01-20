from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.models.bookings import PickupMethod, PickupStatus, PackageType

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
    customer_id: Optional[int] = None
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
