import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.customers import Customer
from app.models.enums import Category, Type,VerificationStatus
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
        try:
            # Ensure consistent case usage
            enum_value_name = enum_value.name  # This returns "tier_1", "individual", etc.

            if field_name == 'customer_category':
                category_enum = Category.__members__.get(enum_value_name)
                if category_enum is None:
                    raise ValueError(f"Invalid CustomerCategory value: {enum_value_name}")

            elif field_name == 'customer_type':
                customer_type_enum = Type.__members__.get(enum_value_name)
                if customer_type_enum is None:
                    raise ValueError(f"Invalid value {enum_value_name} for customer_type enum")
            else:
                raise ValueError(f"Invalid field name: {field_name}")

            # Prepare customer data
            customer_data = {
                "customer_name": f"Dummy {enum_value_name.replace('_', ' ').title()} Customer",
                "customer_mobile": "0000000000",
                "customer_email": f"dummy_{enum_value_name.lower()}@example.com",
                "customer_address": "123 Dummy Street",
                "customer_city": "Dummy City",
                "customer_state": "Dummy State",
                "customer_country": "Dummy Country",
                "customer_pincode": "000000",
                "customer_geolocation": "0.0000° N, 0.0000° W",
                "customer_type": customer_type_enum if field_name == 'customer_type' else Type.individual,
                "customer_category": category_enum if field_name == 'customer_category' else Category.tier_1,
                "verification_status": VerificationStatus.NoneValue.value

            }

            # Add tax_id handling for corporate customers
            if customer_data["customer_type"] == Type.corporate:
                customer_data["tax_id"] = "123-456-789"

            # Check if an entry with the same enum value already exists
            existing_entry = db.query(model).filter(getattr(model, field_name) == enum_value.value).first()
            if not existing_entry:
                db.add(model(**customer_data))
                db.flush()

        except ValueError as e:
            logger.error(f"Error: {str(e)}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error while processing {enum_value}: {str(e)}")
            continue

    db.commit()



# ========== Customer Validation ==========

def check_existing_by_email(db: Session, model, email_field: str, email: str):
    """
    Check if the given email already exists in the specified model.
    """
    field = getattr(model, email_field, None)
    if not field:
        raise ValueError(f"Invalid email field: {email_field}")
    return db.query(model).filter(field == email).first()


def check_existing_by_id_and_email(db: Session, model, id_field: str, email_field: str, id_value: int, email_value: str):
    """
    Generic function to check if a record exists in the given model based on ID and email.
    
    :param db: Database session
    :param model: SQLAlchemy model (Customer, Agent, Associate, etc.)
    :param id_field: The ID field name (e.g., "customer_id", "agent_id")
    :param email_field: The email field name (e.g., "customer_email", "agent_email")
    :param id_value: The ID value to check
    :param email_value: The email value to check
    :return: The matching record if found, otherwise None
    """
    id_attr = getattr(model, id_field, None)
    email_attr = getattr(model, email_field, None)

    if not id_attr or not email_attr:
        raise ValueError(f"Invalid ID field ({id_field}) or email field ({email_field}) for model {model.__name__}")

    return db.query(model).filter(id_attr == id_value, email_attr == email_value).first()


def get_credential_by_id(db: Session, model, id_field: str, id_value: int):
    """
    Generic function to fetch a credential using an ID field.

    :param db: Database session
    :param model: SQLAlchemy model (CustomerCredential, AgentCredential, AssociateCredential, etc.)
    :param id_field: The ID field name (e.g., "customer_id", "agent_id", "associates_id")
    :param id_value: The ID value to check
    :return: The matching credential record if found, otherwise None
    """
    id_attr = getattr(model, id_field, None)

    if id_attr is None:
        raise ValueError(f"Invalid ID field ({id_field}) for model {model.__name__}")

    return db.query(model).filter(id_attr == id_value).first()

