from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.bookings import BookingCreate, BookingDetailedResponse, BookingUpdate,AddressBookCreate, AddressBookResponse, AddressBookUpdate,QuotationCreate, QuotationDetailedResponse, QuotationUpdate
from app.database import get_db
from typing import List
from sqlalchemy.exc import IntegrityError
from app.models import Bookings,Quotations,AddressBook
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import joinedload
from app.crud.bookings import get_booking, create_booking, update_booking, delete_booking, \
                             get_address_book, create_address_book, update_address_book, delete_address_book, \
                             get_quotation, create_quotation, update_quotation, delete_quotation

router = APIRouter()

# Create booking
@router.post("/createbooking/", response_model=BookingDetailedResponse, status_code=status.HTTP_201_CREATED,
             description="Create a new booking and return the created booking object.")
async def create_booking_api(booking: BookingCreate, db: Session = Depends(get_db)):
    try:
        # Pass booking data to CRUD function
        return create_booking(db, booking)
    except IntegrityError as e:
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(status_code=400, detail="Booking with this identifier already exists")
        raise HTTPException(status_code=500, detail="Database error occurred")

# GET booking by ID
@router.get("/{booking_id}/viewbooking/", response_model=BookingDetailedResponse, status_code=status.HTTP_200_OK)
async def get_booking(booking_id: int, db: Session = Depends(get_db)):

    booking = db.query(Bookings).options(joinedload(Bookings.booking_items)).filter(Bookings.booking_id == booking_id).first()
    
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Prepare the response model with data from the booking
    booking_data = {key: value for key, value in booking.__dict__.items() if key != '_sa_instance_state'}
    
    # Ensure that booking_items is included in the response
    booking_data['booking_items'] = [
        {
            'weight': item.weight,
            'length': item.length,
            'width': item.width,
            'height': item.height,
            'package_type': item.package_type,
            'cost': item.cost,
            'item_id': item.item_id,
        }
        for item in booking.booking_items
    ]
    
    # Ensure package_type is set
    if not booking_data.get('package_type'):
        booking_data['package_type'] = "other"  # Default value
    return booking_data

# GET all bookings
@router.get("/allbookings", response_model=List[BookingDetailedResponse])
def get_all_bookings_api(db: Session = Depends(get_db)):
    bookings = db.query(Bookings).all()
    return bookings

# UPDATE booking by ID
@router.put("/{booking_id}/updatebooking", response_model=BookingDetailedResponse, status_code=status.HTTP_200_OK)
async def update_booking_api(booking_id: int, booking: BookingUpdate, db: Session = Depends(get_db)):
    # Convert Pydantic model to dict (only unset fields are excluded)
    booking_data = booking.dict(exclude_unset=True)

    # Validate if essential fields like 'created_by' and 'package_type' are properly provided
    if 'created_by' not in booking_data:
        raise HTTPException(status_code=400, detail="Missing required field: created_by")
    
    # Call the update function with booking data and session
    updated_booking = update_booking(booking_id, booking_data, db)
    
    # If no updated booking is found, raise a not found exception
    if not updated_booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return updated_booking

# DELETE booking by ID with HTTP_204_NO_CONTENT status
@router.delete("/{booking_id}/deletebooking", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking_api(booking_id: int, db: Session = Depends(get_db)):
    db_booking = get_booking(db, booking_id)
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    delete_booking(db, booking_id)
    return {"status": "success", "message": f"Booking (ID: {booking_id}) deleted successfully"}

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

# Create address book
@router.post("/createaddressbook/", response_model=AddressBookResponse, status_code=status.HTTP_201_CREATED,
             description="Create a new address book entry and return the created entry.")
async def create_address_book_api(address: AddressBookCreate, db: Session = Depends(get_db)):
    try:
        # Pass address data to CRUD function
        return create_address_book(db, address)
    except IntegrityError as e:
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(status_code=400, detail="Address with this identifier already exists")
        raise HTTPException(status_code=500, detail="Database error occurred")

# GET address by ID
@router.get("/{address_id}/viewaddressbook/", response_model=AddressBookResponse, status_code=status.HTTP_200_OK)
async def get_address_book_api(address_id: int, db: Session = Depends(get_db)):
    db_address = get_address_book(db, address_id)
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address    

# GET all address books
@router.get("/alladdressbooks", response_model=List[AddressBookResponse])
def get_all_addresses_api(db: Session = Depends(get_db)):
    addresses = db.query(AddressBook).all()
    return addresses

# UPDATE address by ID
@router.put("/{address_id}/updateaddressbook", response_model=AddressBookResponse, status_code=status.HTTP_200_OK)
async def update_address_book_api(address_id: int, address: AddressBookUpdate, db: Session = Depends(get_db)):
    if not any(value is not None for value in address.dict().values()):
        raise HTTPException(status_code=400, detail="No fields to update")

    updated_address = update_address_book(db, address_id, address.dict(exclude_unset=True))
    return updated_address

# DELETE address by ID
@router.delete("/{address_id}/deleteaddressbook", status_code=status.HTTP_200_OK)
async def delete_address_book_api(address_id: int, db: Session = Depends(get_db)):
    db_address = get_address_book(db, address_id)
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    delete_address_book(db, address_id)
    return {"detail": f"Address (ID: {address_id}) deleted successfully"}