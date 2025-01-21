from fastapi import HTTPException
from sqlalchemy.orm import Session
import logging
from app.models.customers import Customer
from app.models.enums import CustomerCategory, CustomerType

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Reusable function to populate dynamic entries (categories, customer types, etc.)
# Corrected Enum handling in populate_dynamic_entries
def populate_dynamic_entries(db: Session, model, enum_list, field_name: str):
    for enum_value in enum_list:
        enum_value_correct = enum_value  # The actual Enum member

        # Handle 'customer_category' correctly
        if field_name == 'customer_category':

            category_enum = getattr(CustomerCategory, enum_value_correct, None)
            if category_enum is None:
               raise ValueError(f"Invalid CustomerCategory value: {enum_value_correct}")

        # Prepare customer data using enum value correctly
        customer_data = {
            "customer_name": f"Dummy {enum_value_correct.replace('_', ' ').title()} Customer",
            "customer_mobile": "0000000000",
            "customer_email": f"dummy_{enum_value_correct.replace('_', ' ').lower()}@example.com",
            "customer_address": "123 Dummy Street",
            "customer_city": "Dummy City",
            "customer_state": "Dummy State",
            "customer_country": "Dummy Country",
            "customer_pincode": "000000",
            "customer_geolocation": "0.0000° N, 0.0000° W",
            "customer_type": getattr(CustomerType, enum_value_correct, CustomerType.individual),
            "customer_category": category_enum if field_name == 'customer_category' else CustomerCategory.tier_1,
            "verification_status": "Verified",
            "is_active": True,
        }

        # Check if an entry with the same enum value already exists
        existing_entry = db.query(model).filter(getattr(model, field_name) == enum_value_correct).first()

        if not existing_entry:
            db.add(model(**customer_data))

    db.commit()



# Generalized validator for checking the existence of a model entry by ID
def validate_entry_by_id(value: int, db: Session, model, field_name: str):
    if not hasattr(model, field_name):
        raise HTTPException(status_code=400, detail=f"Invalid field: {field_name}")
    entry = db.query(model).filter(getattr(model, field_name) == value).first()
    if not entry:
        raise HTTPException(status_code=400, detail=f"Invalid {field_name} ID")
    return value

# Generalized foreign key validator
def validate_foreign_key(db: Session, model, field: str, value: int):
    obj = db.query(model).filter(getattr(model, field) == value).first()
    if not obj:
        raise HTTPException(status_code=400, detail=f"Invalid {field} ID")
    return value

# Generalized function to get an entity by ID
def get_entity_by_id(db: Session, model, entity_id: int, field_name: str):
    entity = db.query(model).filter(getattr(model, field_name) == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return entity

# Function to log errors and raise HTTP exceptions
def log_and_raise_exception(error_message: str, status_code: int = 400):
    logger.error(error_message)
    raise HTTPException(status_code=status_code, detail=error_message)

def check_duplicate_email_or_mobile(db, model, email: str, mobile: str):
    return db.query(model).filter(
        (model.email == email) | (model.mobile == mobile)
    ).first()

# app/utils.py
def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.customer_email == email).first()
