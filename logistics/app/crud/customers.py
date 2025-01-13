from sqlalchemy.orm import Session, joinedload
from app.models.customers import Customer, CustomerCategory, CustomerType
from app.utils import validate_entry_by_id, log_and_raise_exception, get_entity_by_id,populate_dynamic_entries

# Fetches all customers from the database.
def get_all_customers(db: Session):
    """
    Retrieve all customers from the database with their booking details.
    """
    try:
        return db.query(Customer).options(joinedload(Customer.customer_type)).all()
    except Exception as e:
        log_and_raise_exception(f"Error fetching all customers: {str(e)}", 500)

# Fetches a customer by ID.
def get_customer(db: Session, customer_id: int):
    """
    Retrieve a user by their ID.
    """
    return get_entity_by_id(db, Customer, customer_id, 'customer_id')

# Creates a new customer in the database.
def create_customer(db: Session, customer_data: dict):
    """
    Create a new user in the database.
    """
    try:
        validate_entry_by_id(customer_data['category_id'], db, CustomerCategory, 'id')
        validate_entry_by_id(customer_data['type_id'], db, CustomerType, 'id')

        db_customer = Customer(**customer_data)
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error creating customer: {str(e)}", 500)

# Updates a customer by ID.
def update_customer(db: Session, customer_id: int, customer_data: dict):
    """
    Update an existing customer by their ID.
    """
    existing_customer = get_entity_by_id(db, Customer, customer_id, 'customer_id')
    try:
        if 'category_id' in customer_data:
            validate_entry_by_id(customer_data['category_id'], db, CustomerCategory, 'id')

        if 'type_id' in customer_data:
            validate_entry_by_id(customer_data['type_id'], db, CustomerType, 'id')

        for key, value in customer_data.items():
            setattr(existing_customer, key, value)

        db.commit()
        db.refresh(existing_customer)
        return existing_customer
    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error updating customer with ID {customer_id}: {str(e)}", 500)

# Deletes a customer by ID.
def delete_customer(db: Session, customer_id: int):
    """
    Delete a customer by their ID.
    """
    customer_to_delete = get_entity_by_id(db, Customer, customer_id, 'customer_id')
    try:
        db.delete(customer_to_delete)
        db.commit()
        return {"detail": f"Customer {customer_to_delete.name} (ID: {customer_to_delete.customer_id}) deleted successfully"}
    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error deleting customer with ID {customer_id}: {str(e)}", 500)

# Populate categories dynamically
def populate_categories(db: Session):
    categories = ["individual", "company", "business", "customs_agent", "carrier"]
    populate_dynamic_entries(db, CustomerCategory, categories)

# Populate customer types dynamically
def populate_customer_types(db: Session):
    types = ["regular", "premium", "enterprise", "freelancer", "agency"]
    populate_dynamic_entries(db, CustomerType, types)