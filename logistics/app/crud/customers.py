from sqlalchemy.orm import Session, joinedload
from app.models.customers import Customer, CustomerCategory, CustomerType
from fastapi import HTTPException
import logging

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Reusable function to populate dynamic entries (categories, customer types, etc.)
def populate_dynamic_entries(db: Session, model, entries: list):
    for entry in entries:
        if not db.query(model).filter(model.name == entry).first():
            db.add(model(name=entry))
    db.commit()

# Fetches all customers from the database.
def get_all_customers(db: Session):
    """
    Retrieve all customers from the database with their customer type.
    """
    try:
        return db.query(Customer).options(joinedload(Customer.customer_type)).all()
    except Exception as e:
        logger.error(f"Error fetching all customers: {str(e)}")
        raise

# Fetches a customer by ID.
def get_customer(db: Session, customer_id: int):
    """
    Retrieve a customer by their ID.
    """
    try:
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except Exception as e:
        logger.error(f"Error fetching customer with ID {customer_id}: {str(e)}")
        raise

# Creates a new customer in the database.
def create_customer(db: Session, customer_data: dict):
    """
    Create a new customer in the database.
    """
    try:
        # Validate category_id
        category = db.query(CustomerCategory).filter(CustomerCategory.id == customer_data['category_id']).first()
        if not category:
            raise HTTPException(status_code=400, detail="Invalid category ID")

        # Validate type_id
        customer_type = db.query(CustomerType).filter(CustomerType.id == customer_data['type_id']).first()
        if not customer_type:
            raise HTTPException(status_code=400, detail="Invalid type ID")

        db_customer = Customer(**customer_data)
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating customer: {str(e)}")
        raise

# Updates a customer by ID.
def update_customer(db: Session, customer_id: int, customer_data: dict):
    """
    Update an existing customer by their ID.
    """
    try:
        existing_customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not existing_customer:
            raise HTTPException(status_code=404, detail="Customer ID not found")

        # Validate category_id if it is being updated
        if 'category_id' in customer_data:
            category = db.query(CustomerCategory).filter(CustomerCategory.id == customer_data['category_id']).first()
            if not category:
                raise HTTPException(status_code=400, detail="Invalid category ID")

        # Validate type_id if it is being updated
        if 'type_id' in customer_data:
            customer_type = db.query(CustomerType).filter(CustomerType.id == customer_data['type_id']).first()
            if not customer_type:
                raise HTTPException(status_code=400, detail="Invalid type ID")

        # Update fields dynamically
        for key, value in customer_data.items():
            setattr(existing_customer, key, value)

        db.commit()
        db.refresh(existing_customer)
        return existing_customer
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating customer with ID {customer_id}: {str(e)}")
        raise

# Deletes a customer by ID.
def delete_customer(db: Session, customer_id: int):
    """
    Delete a customer by their ID.
    """
    try:
        customer_to_delete = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer_to_delete:
            raise HTTPException(status_code=404, detail="Customer ID not found")

        db.delete(customer_to_delete)
        db.commit()
        return {"detail": f"Customer {customer_to_delete.name} (ID: {customer_to_delete.id}) deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting customer with ID {customer_id}: {str(e)}")
        raise

# Populate categories dynamically
def populate_categories(db: Session):
    """
    Populate customer categories if they don't already exist.
    """
    categories = [
        "individual",
        "company",
        "business",
        "customs_agent",
        "carrier"
    ]
    populate_dynamic_entries(db, CustomerCategory, categories)

# Populate customer types dynamically
def populate_customer_types(db: Session):
    """
    Populate customer types if they don't already exist.
    """
    types = [
        "regular",
        "premium",
        "enterprise",
        "freelancer",
        "agency"
    ]
    populate_dynamic_entries(db, CustomerType, types)

def validate_category_id(value: int, db: Session):
    """
    Validate a category ID.
    """
    try:
        category = db.query(CustomerCategory).filter(CustomerCategory.id == value).first()
        if not category:
            raise HTTPException(status_code=400, detail="Invalid category ID")
        return value
    except Exception as e:
        logger.error(f"Error validating category ID {value}: {str(e)}")
        raise