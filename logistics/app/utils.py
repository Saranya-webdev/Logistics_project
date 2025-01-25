import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
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
def log_and_raise_exception(message: str, status_code: int):
    """Logs the exception and raises an HTTPException."""
    logger.error(message)  # Make sure you have a logger defined
    raise HTTPException(status_code=status_code, detail=message)

# ========== Core Business Logic Functions ==========

def populate_dynamic_entries(db: Session, model, enum_list, field_name: str):
    """Populate dynamic entries in the database based on enum values."""
    for enum in enum_list:
        try:
            # Convert enum to name (or value if required)
            enum_name = enum.name  # Get the enum name
            enum_value = enum.value  # Get the enum value

            if field_name == "customer_category":
                if enum_name not in Category.__members__:
                    raise ValueError(f"Invalid CustomerCategory value: {enum_name}")
                category_enum_value = enum_value  # Use enum.value for insertion

            elif field_name == "customer_type":
                if enum_name not in Type.__members__:
                    raise ValueError(f"Invalid CustomerType value: {enum_name}")
                customer_type_enum_value = enum_value  # Use enum.value for insertion

            else:
                raise ValueError(f"Unknown field_name: {field_name}")

            # Build customer data
            customer_data = {
                "customer_name": f"Dummy {enum_name.replace('_', ' ').title()} Customer",
                "customer_mobile": "0000000000",
                "customer_email": f"dummy_{enum_name.replace('_', ' ').lower()}@example.com",
                "customer_address": "123 Dummy Street",
                "customer_city": "Dummy City",
                "customer_state": "Dummy State",
                "customer_country": "Dummy Country",
                "customer_pincode": "000000",
                "customer_geolocation": "0.0000° N, 0.0000° W",
                "customer_type": customer_type_enum_value if field_name == "customer_type" else Type.individual.value,
                "customer_category": category_enum_value if field_name == "customer_category" else Category.tier_1.value,
                "verification_status": "Verified",
                "is_active": True,
            }

            # Add tax_id for corporate customers
            if customer_data["customer_type"] == Type.corporate.value:
                customer_data["tax_id"] = "123-456-789"

            # Check if an entry with the same enum value exists
            existing_entry = db.query(model).filter(getattr(model, field_name) == enum_value).first()

            if not existing_entry:
                db.add(model(**customer_data))
                db.flush()

        except ValueError as e:
            logger.error(f"Error: {str(e)}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error while processing {enum_name}: {str(e)}")
            continue

    db.commit()



# ========== Customer Validation ==========

def check_existing_by_email(db: Session, model, email_field: str, email: str):
    """
    Check if the given email already exists in the specified model.
    
    Args:
        db (Session): The database session.
        model: The SQLAlchemy model to query (e.g., Customer, Agent, Carrier).
        email_field (str): The name of the email field in the model.
        email (str): The email to check for existence.
    
    Returns:
        The first matching record if found, otherwise None.
    """
    field = getattr(model, email_field, None)
    if not field:
        raise ValueError(f"Invalid email field: {email_field}")
    return db.query(model).filter(getattr(model, email_field) == email).first() is not None



# ========== Agent Validation ==========

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


