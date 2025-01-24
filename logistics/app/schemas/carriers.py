from pydantic import BaseModel
from typing import Optional

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
    active_flag: int
    remarks: Optional[str] = None

class AgentCreate(BaseModel):
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

class AgentUpdate(BaseModel):
    carrier_name: Optional[str] = None
    carrier_email: Optional[str] = None
    carrier_mobile: Optional[str] = None
    carrier_address: Optional[str] = None
    carrier_city: Optional[str] = None
    carrier_state: Optional[str] = None
    carrier_country: Optional[str] = None
    carrier_pincode: Optional[str] = None
    carrier_geolocation: Optional[str] = None
    remarks: Optional[str] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class AgentUpdateResponse(BaseModel):
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


class AgentResponse(BaseModel):
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


class AgentBookingListResponse(BaseModel):
    carrier_id: int
    carrier_name: str
    carrier_mobile: str
    carrier_email: str
    carrier_address: str
    carrier_city: str
    carrier_state: str
    carrier_country: str
    carrier_pincode: Optional[str]
    carrier_geolocation: Optional[str]

    class Config:
        from_attributes = True