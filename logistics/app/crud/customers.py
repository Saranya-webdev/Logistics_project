from sqlalchemy.orm import Session, joinedload
from app.models import Customer
from fastapi import HTTPException
from app.models import CustomerCategory, CustomerType


# Reusable function to populate dynamic entries (categories, customer types, etc.)
def populate_dynamic_entries(db: Session, model, entries: list):
    for entry in entries:
        if not db.query(model).filter(model.name == entry).first():
            db.add(model(name=entry))
    db.commit()


# Fetches all customers from the database.
def get_all_customers(db):
    return db.query(Customer).options(joinedload(Customer.customer_type)).all()

# Fetches a customer by ID.
def get_customer(db: Session, customer_id: int):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


# Creates a new customer in the database.
def create_customer(db: Session, customer_data: dict):
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


# Updates a customer by ID.
def update_customer(db: Session, customer_id: int, customer_data: dict):
    existing_customer = db.query(Customer).filter(Customer.id == customer_id).first()
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


# Deletes a customer by ID.
def delete_customer(db: Session, customer_id: int):
    customer_to_delete = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer_to_delete:
        raise HTTPException(status_code=404, detail="Customer ID not found")

    db.delete(customer_to_delete)
    db.commit()
    return {"detail": f"Customer {customer_to_delete.name} (ID: {customer_to_delete.id}) deleted successfully"}


# Populate categories dynamically
def populate_categories(db: Session):
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
    types = [
        "regular",
        "premium",
        "enterprise",
        "freelancer",
        "agency"
    ]
    populate_dynamic_entries(db, CustomerType, types)


def validate_category_id(value: int, db: Session):
    category = db.query(CustomerCategory).filter(CustomerCategory.id == value).first()
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category ID")
    return value