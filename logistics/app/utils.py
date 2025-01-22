import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.customers import Customer
from app.models.enums import CustomerCategory, CustomerType

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ========== Utility Functions ==========

# Generalized validator for checking the existence of a model entry by ID
def validate_entry_by_id(value: int, db: Session, model, field_name: str):
    """Validate if the entry exists in the model by ID."""
    if not hasattr(model, field_name):
        raise HTTPException(status_code=400, detail=f"Invalid field: {field_name}")
    entry = db.query(model).filter(getattr(model, field_name) == value).first()
    if not entry:
        raise HTTPException(status_code=400, detail=f"Invalid {field_name} ID")
    return value

# Generalized foreign key validator
def validate_foreign_key(db: Session, model, field: str, value: int):
    """Validate if the foreign key exists in the model."""
    obj = db.query(model).filter(getattr(model, field) == value).first()
    if not obj:
        raise HTTPException(status_code=400, detail=f"Invalid {field} ID")
    return value

# Generalized function to get an entity by ID
def get_entity_by_id(db: Session, model, entity_id: int, field_name: str):
    """Get an entity by its ID."""
    entity = db.query(model).filter(getattr(model, field_name) == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return entity

# Function to log errors and raise HTTP exceptions
def log_and_raise_exception(error_message: str, status_code: int = 400):
    """Log an error and raise an HTTP exception."""
    logger.error(error_message)
    raise HTTPException(status_code=status_code, detail=error_message)

# ========== Core Business Logic Functions ==========

def populate_dynamic_entries(db: Session, model, enum_list, field_name: str):
    """Populate dynamic entries in the database based on enum values."""
    for enum_value in enum_list:
        enum_value_correct = enum_value  # The actual Enum member

        try:
            # Handle enums dynamically based on the field name
            if field_name == 'customer_category':
                category_enum = getattr(CustomerCategory, enum_value_correct, None)
                if category_enum is None:
                    raise ValueError(f"Invalid CustomerCategory value: {enum_value_correct}")
            elif field_name == 'customer_type':
                # Get the actual enum member from CustomerType
                customer_type_enum = getattr(CustomerType, enum_value_correct, None)
                if customer_type_enum is None:
                    raise ValueError(f"Invalid value {enum_value_correct} for customer_type enum")
            else:
                # Try fetching the enum from the model dynamically
                field_enum = getattr(model, field_name, None)
                if field_enum is None:
                    raise ValueError(f"Invalid field name: {field_name} for model: {model}")
                field_enum_value = getattr(field_enum, enum_value_correct, None)
                if field_enum_value is None:
                    raise ValueError(f"Invalid value {enum_value_correct} for {field_name} enum")

            # Prepare customer data without dummy values
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
                "customer_type": customer_type_enum if field_name == 'customer_type' else getattr(CustomerType, "individual"),
                "customer_category": category_enum if field_name == 'customer_category' else CustomerCategory.tier_1,
                "verification_status": "Verified",
                "is_active": True,
            }

            # Add tax_id handling for corporate customers (if applicable)
            if customer_data["customer_type"] == CustomerType.corporate:
                customer_data["tax_id"] = "123-456-789"  # Example tax_id, adjust based on actual logic

            # Check if an entry with the same enum value already exists
            existing_entry = db.query(model).filter(getattr(model, field_name) == enum_value_correct).first()

            if not existing_entry:
                db.add(model(**customer_data))
                
                # Flush to the database after adding
                db.flush()

        except ValueError as e:
            logger.error(f"Error: {str(e)}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error while processing {enum_value_correct}: {str(e)}")
            continue

    db.commit()

# ========== Customer Validation ==========

def check_existing_customer(db: Session, email: str):
    """Check if a customer with the given email already exists."""
    return db.query(Customer).filter(Customer.customer_email == email).first()
