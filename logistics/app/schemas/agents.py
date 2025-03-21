from pydantic import BaseModel
from typing import Optional, List
from app.models.enums import Category, VerificationStatus
from datetime import date


class Agent(BaseModel):
    agent_name: str
    agent_email: str
    agent_mobile: str
    agent_address: str
    agent_city: str
    agent_state: str
    agent_country: str
    agent_pincode: Optional[str] = None
    agent_geolocation: str
    agent_category: Category
    agent_businessname: Optional[str] = None
    tax_id: Optional[str] = None
    verification_status: VerificationStatus
    active_flag: int

class AgentCreate(BaseModel):
    agent_name: str
    agent_email: Optional[str] = None
    agent_mobile: str
    agent_address: Optional[str] = None
    agent_city: Optional[str] = None
    agent_state: Optional[str] = None
    agent_country: Optional[str] = None
    agent_pincode: Optional[str] = None
    agent_geolocation: Optional[str] = None
    agent_category: Optional[str] = None
    agent_businessname: Optional[str] = None
    tax_id: Optional[str] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class AgentUpdate(BaseModel):
    agent_name: Optional[str] = None
    agent_email: Optional[str] = None
    agent_mobile: Optional[str] = None
    agent_address: Optional[str] = None
    agent_city: Optional[str] = None
    agent_state: Optional[str] = None
    agent_country: Optional[str] = None
    agent_pincode: Optional[str] = None
    agent_geolocation: Optional[str] = None
    agent_businessname: Optional[str] = None
    tax_id: Optional[str] = None
    agent_category: Category


    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class AgentUpdateResponse(BaseModel):
    agent_id: int
    agent_name: str
    agent_email: str
    agent_mobile: str
    agent_address: str
    agent_city: str
    agent_state: str
    agent_country: str
    agent_pincode: Optional[str] = None
    agent_geolocation: str
    agent_category: Category
    agent_businessname: Optional[str] = None
    tax_id: Optional[str] = None
    verification_status: str
    active_flag: Optional[int] = None  

    class Config:
        from_attributes = True
  
       


class AgentResponse(BaseModel):
    agent_id: int
    agent_name: str
    agent_email: str
    agent_mobile: str
    agent_address: str
    agent_city: str
    agent_state: str
    agent_country: str
    agent_pincode: Optional[str] = None
    agent_geolocation: str
    agent_category: Category
    agent_businessname: Optional[str] = None
    tax_id: Optional[str] = None
    remarks: Optional[str] = None
    verification_status: str
    active_flag: int
    

    class Config:
        from_attributes = True

class AgentBookingItems(BaseModel):
    item_id: int
    item_weight: float
    item_length: float
    item_width: float
    item_height: float
    package_type: str 

class AgentBookings(BaseModel):
    booking_id: int
    customer_id: int
    booking_by: str
    from_city: str
    from_pincode: str
    to_city: str
    to_pincode: str
    carrier_plan: str
    carrier_name: str
    est_delivery_date: date
    pickup_date: str
    pickup_time: str
    package_count: str
    total_cost: str
    booking_status: str
    booking_items:List[AgentBookingItems] = []


class AgentBookingListResponse(BaseModel):
    agent_email: str
    bookings: List[AgentBookings]
    
    class Config:
        from_attributes = True
 
class SuspendOrActiveRequest(BaseModel):
    agent_email: str
    active_flag: int
    remarks: str

    class Config:
        from_attributes = True

class SuspendOrActiveResponse(BaseModel):
    agent_id: int
    agent_name: str
    agent_email: str
    agent_mobile: str
    verification_status: Optional[VerificationStatus] = None
    remarks: Optional[str] = None
    active_flag: int

    class Config:
        from_attributes = True


class VerifyStatusRequest(BaseModel):
    agent_email: str
    verification_status: VerificationStatus

class VerifyStatusResponse(BaseModel):
    agent_id: int
    agent_name: str
    agent_email: str
    agent_mobile: str
    verification_status: Optional[VerificationStatus] = None
    remarks: Optional[str] = None
    active_flag: int

    class Config:
        from_attributes = True


class AgentCredentialCreate(BaseModel):
    agent_id: int
    agent_email: str
    password: str

class AgentCredentialResponse(BaseModel):
    agent_credential_id: int
    agent_id: int
    email_id: str
     
    class Config:
        from_attributes = True 

class AgentPasswordUpdate(BaseModel):
    agent_id: int
    new_password: str          