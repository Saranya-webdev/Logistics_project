from fastapi import HTTPException
from sqlalchemy.orm import Session

# Reusable function to populate dynamic entries (categories, customer types, etc.)
def populate_dynamic_entries(db: Session, model, entries: list):
    for entry in entries:
        if not db.query(model).filter(model.name == entry).first():
            db.add(model(name=entry))
    db.commit()

# Generalized validator for checking the existence of a model entry by ID
def validate_entry_by_id(value: int, db: Session, model, field_name: str):
    entry = db.query(model).filter(getattr(model, field_name) == value).first()
    if not entry:
        raise HTTPException(status_code=400, detail=f"Invalid {field_name} ID")
    return value


def validate_foreign_key(db: Session, model, field: str, value: int):
    obj = db.query(model).filter(getattr(model, field) == value).first()
    if not obj:
        raise HTTPException(status_code=400, detail=f"Invalid {field} ID")
    return value

def get_entity_by_id(db: Session, model, entity_id: int):
    # Use getattr to dynamically fetch the correct field name (e.g., 'user_id' instead of 'id')
    entity = db.query(model).filter(getattr(model, 'user_id') == entity_id).first()  # Adjust 'user_id' based on the actual field name
    if not entity:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return entity
