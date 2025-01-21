from pydantic import BaseModel, root_validator
from typing import Optional, List
from app.models.customers import CustomerCategory, CustomerType

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
    customer_type: CustomerType
    customer_category: CustomerCategory
    notes: Optional[str] = None
    verification_status: str
    # Add business-related fields for corporate customers
    tax_id: Optional[str] = None
    license_number: Optional[str] = None
    designation: Optional[str] = None
    company_name: Optional[str] = None


    @root_validator(pre=True)
    def check_business_fields(cls, values):
        # Enforce that business fields are required if customer_type is 'business'
        if values.get("customer_type") == CustomerType.corporate:
            required_business_fields = ["tax_id", "license_number", "designation", "company_name"]
            missing_fields = [field for field in required_business_fields if not values.get(field)]
            if missing_fields:
                raise ValueError(f"Missing business fields: {', '.join(missing_fields)}")
        return values

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class CustomerResponse(BaseModel):
    customer_name: str
    customer_email: str
    customer_mobile: str
    customer_address: str
    customer_city: str
    customer_state: str
    customer_country: str
    customer_geolocation: str
    customer_type: str
    customer_category: str
    verification_status: str  # Ensure this field is included
    tax_id: Optional[str]  # Make sure these fields are Optional if not always present
    license_number: Optional[str]
    designation: Optional[str]
    company_name: Optional[str]

    class Config:
        from_attributes = True
     