from pydantic import BaseModel
from typing import Optional, List
from app.models.enums import VerificationStatus, Role

class Associates(BaseModel):
    associates_name: str
    associates_email: str
    associates_mobile: str
    verification_status: VerificationStatus
    active_flag: int = 1
    remarks: Optional[str] = None

class AssociatesCreate(BaseModel):
    associates_name: str
    associates_email: Optional[str] = None
    associates_mobile: str
    associates_role: Role
    verification_status: Optional[VerificationStatus] = VerificationStatus.pending

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class AssociatesUpdate(BaseModel):
    associates_name: Optional[str] = None
    associates_email: Optional[str] = None
    associates_mobile: Optional[str] = None
    associates_role: Optional[Role] = None
    remarks: Optional[str] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class AssociatesUpdateResponse(BaseModel):
    associates_id: int
    associates_name: str
    associates_email: str
    associates_mobile: str
    associates_role: Role
    verification_status: VerificationStatus
    active_flag: Optional[int] = None 
    remarks: Optional[str] = None      


class AssociatesResponse(BaseModel):
    associates_id: int
    associates_name: str
    associates_email: str
    associates_mobile: str
    associates_role: Role
    verification_status: VerificationStatus
    remarks: Optional[str] = None
    active_flag: int
    
    class Config:
        from_attributes = True


class SuspendOrActiveRequest(BaseModel):
    associates_email: str
    active_flag: int
    remarks: str

class SuspendOrActiveResponse(BaseModel):
    associates_id: int
    associates_name: str
    associates_email: str
    associates_mobile: str
    associates_role: str
    verification_status: Optional[VerificationStatus] = None
    remarks: Optional[str] = None
    active_flag: int

    class Config:
        from_attributes = True

class VerifyStatusRequest(BaseModel):
    associates_email: str
    verification_status: VerificationStatus

class VerifyStatusResponse(BaseModel):
    associates_id: int
    associates_name: str
    associates_email: str
    associates_mobile: str
    associates_role: Role
    verification_status: Optional[VerificationStatus] = None
    remarks: Optional[str] = None
    active_flag: int

    class Config:
        from_attributes = True   


class AssociatesCredentialCreate(BaseModel):
    associates_id: int
    associates_email: str
    password: str

class AssociatesCredentialResponse(BaseModel):
    associates_credential_id: int
    associates_id: int
    email_id: str
     
    class Config:
        from_attributes = True 

class AssociatesPasswordUpdate(BaseModel):
    associates_id: int
    new_password: str        


class AssociateBookingItems(BaseModel):
    item_id: int
    item_weight: float
    item_length: float
    item_width: float
    item_height: float
    package_type: str 

class AssociateBookings(BaseModel):
    booking_id: int
    customer_id: int
    booking_by: str
    from_name: str
    to_name: str
    carrier_name: str
    pickup_date: str
    package_count: str
    total_cost: str
    booking_status: str
    booking_items:List[AssociateBookingItems] = []


class AssociateBookingListResponse(BaseModel):
    associates_email: str
    bookings: List[AssociateBookings]
    
    class Config:
        from_attributes = True    