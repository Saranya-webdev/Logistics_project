from pydantic import BaseModel, root_validator, Field
from typing import Optional, List
from app.models.enums import Type, Category, VerificationStatus
from app.schemas.bookings import BookingDetailedResponse

class Customer(BaseModel):
    customer_name: str
    customer_email: str
    customer_mobile: str
    customer_address: str
    customer_city: str
    customer_state: str
    customer_country: str
    customer_pincode: Optional[str] = None
    customer_geolocation: str
    customer_type: str
    customer_category: str
    verification_status: VerificationStatus
    active_flag: int

class CustomerCreate(BaseModel):
    customer_name: str
    customer_email: str
    customer_mobile: str
    customer_address: str
    customer_city: str
    customer_state: str
    customer_country: str
    customer_pincode: Optional[str] = None
    customer_geolocation: str
    customer_type: Type
    customer_category: Category

    # Business-related fields for corporate customers
    tax_id: Optional[str] = None
    license_number: Optional[str] = None
    designation: Optional[str] = None
    company_name: Optional[str] = None

    @root_validator(pre=True)
    def check_business_fields(cls, values):
        customer_type = values.get("customer_type")
        if customer_type == Type.corporate:
            required_fields = ["tax_id", "license_number", "designation", "company_name"]
            missing = [field for field in required_fields if not values.get(field)]
            if missing:
                raise ValueError(f"Missing required fields for corporate customer: {', '.join(missing)}")
        elif customer_type == Type.individual:
            # Set business-related fields to None for individual customers
            for field in ["tax_id", "license_number", "designation", "company_name"]:
                values[field] = None
        return values

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_mobile: Optional[str] = None
    customer_address: Optional[str] = None
    customer_city: Optional[str] = None
    customer_state: Optional[str] = None
    customer_country: Optional[str] = None
    customer_pincode: Optional[str] = None
    customer_geolocation: Optional[str] = None
    customer_type: Optional[Type] = None
    customer_category: Optional[Category] = None
    # remarks: Optional[str] = None
    # verification_status: Optional[str] = None

    # Business-related fields
    tax_id: Optional[str] = None
    license_number: Optional[str] = None
    designation: Optional[str] = None
    company_name: Optional[str] = None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class CustomerUpdateResponse(BaseModel):
    customer_id: int
    customer_name: str
    customer_email: str
    customer_mobile: str
    customer_address: str
    customer_city: str
    customer_state: str
    customer_country: str
    customer_pincode: Optional[str] = None
    customer_geolocation: str
    customer_type: Type
    customer_category: Category
    # verification_status: VerificationStatus
    # active_flag: Optional[int] = None
    business_id: Optional[int] = None
    tax_id: Optional[str] = None
    license_number: Optional[str] = None
    designation: Optional[str] = None
    company_name: Optional[str] = None

class CustomerResponse(BaseModel):
    customer_id: int
    customer_name: str
    customer_email: str
    customer_mobile: str
    customer_address: str
    customer_city: str
    customer_state: str
    customer_country: str
    customer_pincode: Optional[str] = None
    customer_geolocation: str
    customer_type: Type
    customer_category: Category
    # remarks: Optional[str] = None
    verification_status: VerificationStatus
    active_flag: int
    # Business-related fields
    business_id: Optional[int] = None
    tax_id: Optional[str] = None
    license_number: Optional[str] = None
    designation: Optional[str] = None
    company_name: Optional[str] = None

    class Config:
        from_attributes = True


class CustomerBookingListResponse(BaseModel):
    customer_id: int
    customer_name: str
    customer_mobile: str
    customer_email: str
    customer_address: str
    customer_city: str
    customer_state: str
    customer_country: str
    customer_pincode: Optional[str] = None

    # Business-related fields
    business_id: Optional[int] = None
    tax_id: Optional[str] = None
    license_number: Optional[str] = None
    designation: Optional[str] = None
    company_name: Optional[str] = None
    # bookings: List[BookingSummary] = []
    bookings:List[BookingDetailedResponse] = [] 


class BookingListResponse(BaseModel):
    bookings: List[CustomerBookingListResponse] = []



class SuspendOrActiveRequest(BaseModel):
    customer_email: str
    active_flag: int
    remarks: str

class SuspendOrActiveResponse(BaseModel):
    customer_id: int
    customer_name: str
    customer_email: str
    customer_mobile: str
    verification_status: Optional[VerificationStatus] = None
    remarks: Optional[str] = None
    active_flag: int

    class Config:
        from_attributes = True


class VerifyStatusRequest(BaseModel):
    customer_email: str
    verification_status: VerificationStatus

class VerifyStatusResponse(BaseModel):
    customer_id: int
    customer_name: str
    customer_email: str
    customer_mobile: str
    verification_status: Optional[VerificationStatus] = None
    remarks: Optional[str] = None
    active_flag: int

    class Config:
        from_attributes = True

class CustomerCredentialCreate(BaseModel):
    customer_id: int
    customer_email: str
    password: str

class CustomerCredentialResponse(BaseModel):
    customer_credential_id: int
    customer_id: int
    email_id: str
     
    class Config:
        from_attributes = True 

class CustomerPasswordUpdate(BaseModel):
    customer_id: int
    new_password: str                