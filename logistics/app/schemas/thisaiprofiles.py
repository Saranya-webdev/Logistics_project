from pydantic import BaseModel
from typing import Optional
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

