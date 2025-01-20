from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session,joinedload
from app.schemas.bookings import BookingCreate, BookingDetailedResponse, BookingUpdate
from app.schemas.addressbook import AddressBookCreate, AddressBookResponse, AddressBookUpdate
from app.schemas.quotations import QuotationCreate, QuotationDetailedResponse, QuotationUpdate
from app.databases.mysqldb import get_db
from typing import List
from sqlalchemy.exc import IntegrityError
from app.models.bookings import Bookings, BookingItem
from app.models.quotations import Quotations
from app.models.addressbooks import AddressBook
from fastapi.exceptions import RequestValidationError
from app.crud.bookings import get_booking, create_booking, update_booking, delete_booking
from app.crud.addressbook import get_address_book, create_address_book, update_address_book, delete_address_book
from app.crud.quotations import get_quotation, create_quotation, update_quotation, delete_quotation

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

