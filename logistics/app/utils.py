import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.customers import Customer
from app.models.agents import Agent
from app.models.enums import Category, Type
from passlib.context import CryptContext


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
                category_enum = getattr(Category, enum_value_correct, None)
                if category_enum is None:
                    raise ValueError(f"Invalid CustomerCategory value: {enum_value_correct}")
            elif field_name == 'customer_type':
                # Get the actual enum member from CustomerType
                customer_type_enum = getattr(Type, enum_value_correct, None)
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
                "customer_type": customer_type_enum if field_name == 'customer_type' else getattr(Type, "individual"),
                "customer_category": category_enum if field_name == 'customer_category' else Category.tier_1,
                "verification_status": "Verified",
                "is_active": True,
            }

            # Add tax_id handling for corporate customers (if applicable)
            if customer_data["customer_type"] == Type.corporate:
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

def check_existing_customer_by_email(db: Session, email: str):
    """Check if a customer with the given email already exists."""
    return db.query(Customer).filter(Customer.customer_email == email).first()


# ========== Agent Validation ==========

def check_existing_agent_by_mobile(db: Session, mobile: str):
    """Check if an agent with the given mobile number already exists."""
    return db.query(Agent).filter(Agent.agent_mobile == mobile).first()


# Initialize a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash the password securely."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify the hashed password against a plain text password."""
    return pwd_context.verify(plain_password, hashed_password)

def process_credentials(agent_data: dict) -> dict:
    """
    Extract and process credentials from the agent data.
    """
    credential_fields = ["email_id", "password"]
    credentials_data = {field: agent_data.pop(field, None) for field in credential_fields}

    # Hash the password if it exists
    if credentials_data.get("password"):
        credentials_data["password"] = hash_password(credentials_data["password"])

    return credentials_data
