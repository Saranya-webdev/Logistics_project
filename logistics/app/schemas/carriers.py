from pydantic import BaseModel
from typing import Optional
from app.models.enums import VerificationStatus

class Carrier(BaseModel):
    carrier_name: str
    carrier_email: str
    carrier_mobile: str
    carrier_address: str
    carrier_city: str
    carrier_state: str
    carrier_country: str
    carrier_pincode: Optional[str] = None
    carrier_geolocation: str
    active_flag: int = 1
    remarks: Optional[str] = None

class CarrierCreate(BaseModel):
    carrier_name: str
    carrier_email: Optional[str] = None
    carrier_mobile: str
    carrier_address: Optional[str] = None
    carrier_city: Optional[str] = None
    carrier_state: Optional[str] = None
    carrier_country: Optional[str] = None
    carrier_pincode: Optional[str] = None
    carrier_geolocation: Optional[str] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class CarrierUpdate(BaseModel):
    carrier_name: Optional[str] 
    carrier_email: Optional[str]
    carrier_mobile: Optional[str]
    carrier_address: Optional[str]
    carrier_city: Optional[str]
    carrier_state: Optional[str]
    carrier_country: Optional[str] 
    carrier_pincode: Optional[str] 
    carrier_geolocation: Optional[str] 
    remarks: Optional[str]

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class CarrierUpdateResponse(BaseModel):
    carrier_id: int
    carrier_name: str
    carrier_email: str
    carrier_mobile: str
    carrier_address: str
    carrier_city: str
    carrier_state: str
    carrier_country: str
    carrier_pincode: Optional[str] = None
    carrier_geolocation: str
    active_flag: Optional[int] = None 
    remarks: Optional[str] = None      


class CarrierResponse(BaseModel):
    carrier_id: int
    carrier_name: str
    carrier_email: str
    carrier_mobile: str
    carrier_address: str
    carrier_city: str
    carrier_state: str
    carrier_country: str
    carrier_pincode: Optional[str] = None
    carrier_geolocation: str
    remarks: Optional[str] = None
    active_flag: int
    
    class Config:
        from_attributes = True

class SuspendOrActiveRequest(BaseModel):
    carrier_email: str
    active_flag: int
    remarks: str

class SuspendOrActiveResponse(BaseModel):
    carrier_id: int
    carrier_name: str
    carrier_email: str
    carrier_mobile: str
    # carrier_role: str
    # verification_status: Optional[VerificationStatus] = None
    remarks: Optional[str] = None
    active_flag: int

    class Config:
        from_attributes = True

     