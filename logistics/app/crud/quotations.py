from sqlalchemy.orm import Session,joinedload
from app.schemas.quotations import  QuotationCreate
from fastapi import HTTPException
import logging
from app.models.quotations import QuotationItems,Quotations
from app.models.quotations import Quotations,QuotationItems 


# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Creates a new quotation in the database
def create_quotation(db: Session, quotation: QuotationCreate):
    """
    Create a new quotation in the database.
    """
    try:
        # Create booking record
        db_quotation = Quotations(
            customer_id=quotation.customer_id,
            created_by=quotation.created_by,
            pickup_method=quotation.pickup_method,
            valid_until=quotation.valid_until,
            created_at=quotation.created_at,
            updated_at=quotation.updated_at,)
        db.add(db_quotation)
        db.commit()
        db.refresh(db_quotation)

        # Add quotation items
        if quotation.quotation_items:
           items_to_add = []
           for item in quotation.quotation_items:
               db_item = QuotationItems(
               quotation_id=db_quotation.quotation_id,
               weight=item.weight,
               length=item.length,
               width=item.width,
               height=item.height,
               package_type=item.package_type,
               cost=item.cost,
               )
               items_to_add.append(db_item)
           db.add_all(items_to_add)
           db.commit()  # Commit after adding all items

        return db_quotation
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating quotation: {str(e)}")
        raise

# Fetches a quotation by ID.
def get_quotation(db: Session, quotation_id: int):
    """
    Retrieve a quotation by their ID.
    """
    try:
        quotation = db.query(Quotations).filter(Quotations.quotation_id == quotation_id).first()
        if not quotation:
            raise HTTPException(status_code=404, detail="Quotation not found")
        return quotation
    except Exception as e:
        logger.error(f"Error fetching quotation with ID {quotation_id}: {str(e)}")
        raise

# Fetches all quotationsfrom the database.
def get_all_quotations(db: Session):
    """
    Retrieve all quotations from the database with their quotation items.
    """
    try:
       return db.query(Quotations).options(joinedload(Quotations.quotation_items)).all()
    except Exception as e:
        logger.error(f"Error fetching all quotations: {str(e)}")
        raise

# Updates a quotation by ID.
def update_quotation(db: Session, quotation_id: int, quotation_data: dict):
    """
    Update an existing quotation by their ID.
    """
    try:
       existing_quotation = db.query(Quotations).filter(Quotations.quotation_id == quotation_id).first()
       if not existing_quotation:
        raise HTTPException(status_code=404, detail="Quotation ID not found")
       
       # Update fields dynamically
       for key, value in quotation_data.items():
            if value is not None:
                setattr(existing_quotation, key, value)
       db.commit()
       db.refresh(existing_quotation)
       return existing_quotation
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating quotation with ID {quotation_id}: {str(e)}")
        raise

# Updates a quotation status by quotation ID.
def update_quotation_status(db: Session, quotation_id: int, status: str):
    """
    Update an existing quotation status by quotation ID.
    """
    try:
       existing_quotation = db.query(Quotations).filter(Quotations.quotation_id == quotation_id).first()
       if existing_quotation:
        existing_quotation.status = status
        db.commit()
        db.refresh(existing_quotation)
        return existing_quotation
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating quotation status with ID {quotation_id}: {str(e)}")
        raise

# Deletes a quotation by ID.
def delete_quotation(db: Session, quotation_id: int):
    """
    Delete a quotation by their ID.
    """
    try:
        quotation_to_delete = db.query(Quotations).filter(Quotations.quotation_id == quotation_id).first()
        if not quotation_to_delete:
            raise HTTPException(status_code=404, detail="Quotation ID not found")

        db.delete(quotation_to_delete)
        db.commit()
        return {"detail": f"Quotation {quotation_to_delete.quotation_id} deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting quotation with ID {quotation_id}: {str(e)}")
        raise

