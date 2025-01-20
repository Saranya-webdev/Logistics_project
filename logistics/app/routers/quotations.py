from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session,joinedload
from app.schemas.quotations import QuotationCreate, QuotationDetailedResponse, QuotationUpdate
from app.databases.mysqldb import get_db
from typing import List
from sqlalchemy.exc import IntegrityError
from app.models.quotations import Quotations
from fastapi.exceptions import RequestValidationError
from app.crud.quotations import get_quotation, create_quotation, update_quotation, delete_quotation

router = APIRouter()

# Create quotation
@router.post("/createquotation/", response_model=QuotationDetailedResponse, status_code=status.HTTP_201_CREATED)
async def create_quotation_api(quotation: QuotationCreate, db: Session = Depends(get_db)):
    try:
        return create_quotation(db, quotation)
    except RequestValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {e.errors()}")
    except IntegrityError as e:
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(status_code=400, detail="Quotation with this identifier already exists")
        raise HTTPException(status_code=500, detail="Database error occurred")

# GET quotation by ID
@router.get("/{quotation_id}/viewquotation/", response_model=QuotationDetailedResponse)
async def get_quotation_api(quotation_id: int, db: Session = Depends(get_db)):
    quotation = (
        db.query(Quotations)
        .options(joinedload(Quotations.quotation_items))
        .filter(Quotations.quotation_id == quotation_id)
        .first()
    )
    if not quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    return QuotationDetailedResponse.from_orm(quotation)   

# GET all quotations
@router.get("/allquotations", response_model=List[QuotationDetailedResponse])
def get_all_quotations_api(db: Session = Depends(get_db)):
    quotations = db.query(Quotations).all()
    return [QuotationDetailedResponse.from_orm(q) for q in quotations]

# UPDATE quotation by ID
@router.put("/{quotation_id}/updatequotation", response_model=QuotationDetailedResponse, status_code=status.HTTP_200_OK)
async def update_quotation_api(quotation_id: int, quotation: QuotationUpdate, db: Session = Depends(get_db)):
    if not any(value is not None for value in quotation.dict().values()):
        raise HTTPException(status_code=400, detail="No fields to update")

    updated_quotation = update_quotation(db, quotation_id, quotation.dict(exclude_unset=True))
    return updated_quotation


# DELETE quotation by ID
@router.delete("/{quotation_id}/deletequotation", status_code=status.HTTP_200_OK)
async def delete_quotation_api(quotation_id: int, db: Session = Depends(get_db)):
    db_quotation = get_quotation(db, quotation_id)
    if not db_quotation:
        raise HTTPException(status_code=404, detail="Quotation not found")
    delete_quotation(db, quotation_id)
    return {"detail": f"Quotation (ID: {quotation_id}) deleted successfully"}

