from fastapi import HTTPException
from sqlalchemy.orm import Session

# Reusable function to populate dynamic entries (categories, customer types, etc.)
def populate_dynamic_entries(db: Session, model, entries: list):
    for entry in entries:
        if not db.query(model).filter(model.name == entry).first():
            db.add(model(name=entry))
    db.commit()

# Generalized validator for checking the existence of a model entry by ID
def validate_entry_by_id(value: int, db: Session, model, model_name: str):
    entry = db.query(model).filter(model.id == value).first()
    if not entry:
        raise HTTPException(status_code=400, detail=f"Invalid {model_name} ID")
    return value


def validate_foreign_key(db: Session, model, field: str, value: int):
    obj = db.query(model).filter(getattr(model, field) == value).first()
    if not obj:
        raise HTTPException(status_code=400, detail=f"Invalid {field} ID")
    return value

def get_entity_by_id(db: Session, model, entity_id: int):
    entity = db.query(model).filter(model.id == entity_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return entity