from pydantic import BaseModel, root_validator, Field
from typing import Optional, List
from app.models.customers import Category, Type
from app.schemas.bookings import BookingSummary

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
    verification_status: str
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
    notes: Optional[str] = None
    verification_status: str

    # Business-related fields for corporate customers
    tax_id: Optional[str] = None
    license_number: Optional[str] = None
    designation: Optional[str] = None
    company_name: Optional[str] = None

    @root_validator(pre=True)
    def check_business_fields(cls, values):
        customer_type = values.get("customer_type")
        required_fields = []  # Initialize it outside the if block

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
    notes: Optional[str] = None
    verification_status: Optional[str] = None

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
    verification_status: str
    active_flag: Optional[int] = None       


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
    notes: Optional[str] = None
    verification_status: str
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
    mobile: str
    email: str
    address: str
    city: str
    state: str
    country: str
    pincode: Optional[str]

    # Business-related fields
    business_id: Optional[int] = None
    tax_id: Optional[str] = None
    license_number: Optional[str] = None
    designation: Optional[str] = None
    company_name: Optional[str] = None
    bookings: List[BookingSummary]