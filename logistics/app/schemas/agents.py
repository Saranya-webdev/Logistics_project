from pydantic import BaseModel, root_validator, Field, validator
from typing import Optional, List
from app.models.enums import Category
from app.schemas.bookings import BookingSummary

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
    email_id: Optional[str] = None
    verification_status: str
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
    email_id: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


    @validator("password")
    def validate_password(cls, value):
        if value and len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return value


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
    email_id: Optional[str] = None
    password: Optional[str] = None

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
    email_id: Optional[str] = None
    verification_status: str
    active_flag: Optional[int] = None       


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
    email_id: Optional[str] = None
    remarks: Optional[str] = None
    verification_status: str
    active_flag: int
    

    class Config:
        from_attributes = True


class AgentBookingListResponse(BaseModel):
    agent_id: int
    agent_name: str
    agent_mobile: str
    agent_email: str
    agent_address: str
    agent_city: str
    agent_state: str
    agent_country: str
    agent_pincode: Optional[str]
    agent_geolocation: Optional[str]
    agent_businessname: Optional[str]
    tax_id: Optional[str]
    bookings: List[BookingSummary]

    class Config:
        from_attributes = True