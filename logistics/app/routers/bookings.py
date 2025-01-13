from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session,joinedload
from app.schemas.bookings import BookingCreate, BookingDetailedResponse, BookingUpdate,AddressBookCreate, AddressBookResponse, AddressBookUpdate,QuotationCreate, QuotationDetailedResponse, QuotationUpdate
from app.databases.mysqldb import get_db
from typing import List
from sqlalchemy.exc import IntegrityError
from app.models.bookings import Bookings, BookingItem
from app.models.quotations import Quotations
from app.models.addressbooks import AddressBook
from fastapi.exceptions import RequestValidationError
from app.crud.bookings import get_booking, create_booking, update_booking, delete_booking, \
                             get_address_book, create_address_book, update_address_book, delete_address_book, \
                             get_quotation, create_quotation, update_quotation, delete_quotation

router = APIRouter()

# Create booking
@router.post("/createbookings/", response_model=BookingDetailedResponse, status_code=status.HTTP_201_CREATED)
async def create_new_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    try:
        new_booking = create_booking(db, booking)
        return new_booking
    except IntegrityError as e:
        if "UNIQUE constraint failed" in str(e.orig):
            raise HTTPException(status_code=400, detail="Booking with this identifier already exists")
        raise HTTPException(status_code=500, detail="Database error occurred")


# GET booking by ID
@router.get("/{booking_id}/viewbooking/", response_model=BookingDetailedResponse, status_code=status.HTTP_200_OK)
async def get_booking(booking_id: int, db: Session = Depends(get_db)):

    # Fetch the booking with its associated items using joinedload
    booking = db.query(Bookings).options(joinedload(Bookings.booking_items)).filter(Bookings.booking_id == booking_id).first()
    
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Prepare the response model with data from the booking
    booking_data = {key: value for key, value in booking.__dict__.items() if key != '_sa_instance_state'}
    
    booking_data['booking_items'] = [
        {
            'item_id': item.item_id,
            'booking_id': booking.booking_id, 
            'weight': item.weight,
            'length': item.length,
            'width': item.width,
            'height': item.height,
            'package_type': item.package_type,
            'cost': item.cost,
        }
        for item in booking.booking_items
    ]
    
    # Ensure package_type is set (if not already set in the booking data)
    if not booking_data.get('package_type'):
        booking_data['package_type'] = "other"  # Default value if package_type is not found

    return booking_data

# GET all bookings
@router.get("/allbookings", response_model=List[BookingDetailedResponse])
def get_all_bookings(db: Session = Depends(get_db)):
    bookings = db.query(Bookings).all()
    return bookings

@router.put("/{booking_id}/updatebooking", response_model=BookingDetailedResponse, status_code=status.HTTP_200_OK)
async def update_booking(booking_id: int, booking: BookingUpdate, db: Session = Depends(get_db)):
    booking_data = booking.dict(exclude_unset=True)

    if 'created_by' not in booking_data:
        raise HTTPException(status_code=400, detail="Missing required field: created_by")

    existing_booking = db.query(Bookings).filter(Bookings.booking_id == booking_id).first()
    if not existing_booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    for key, value in booking_data.items():
        if key != 'booking_items':
            setattr(existing_booking, key, value)

    if 'booking_items' in booking_data:
        for new_item in booking_data['booking_items']:
            if isinstance(new_item, dict):
                new_item_model = BookingItem(**new_item)
            else:
                new_item_model = new_item

            existing_item = db.query(BookingItem).filter(BookingItem.item_id == new_item.get('item_id')).first()
            if existing_item:
                for key, value in new_item.items():
                    setattr(existing_item, key, value)
            else:
                existing_booking.booking_items.append(new_item_model)

    db.commit()
    db.refresh(existing_booking)

    # Ensure booking_id is set for each booking_item before returning
    updated_booking_data = {key: value for key, value in existing_booking.__dict__.items() if key != '_sa_instance_state'}
    updated_booking_data['booking_items'] = [
        {key: getattr(item, key) for key in ['item_id', 'weight', 'length', 'width', 'height', 'package_type', 'cost', 'booking_id']}
        for item in existing_booking.booking_items
    ]
    
    return updated_booking_data




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