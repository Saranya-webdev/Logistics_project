from sqlalchemy.orm import Session
from app.models import Bookings, Quotations, AddressBook, BookingItem, QuotationItems,Users
from app.schemas.bookings import BookingCreate, QuotationCreate, AddressBookCreate,BookingDetailedResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

# CRUD for Booking
def create_booking(db: Session, booking: BookingCreate):
    try:
        # Create booking record
        db_booking = Bookings(
            user_id=booking.user_id,
            created_by=booking.created_by,
            pickup_method=booking.pickup_method,
            booking_status=booking.booking_status,
            name=booking.name,
            phone_number=booking.phone_number,
            email=booking.email,
            address=booking.address,
            city=booking.city,
            state=booking.state,
            country=booking.country,
            pincode=booking.pincode,
            to_name=booking.to_name,
            to_phone_number=booking.to_phone_number,
            to_email=booking.to_email,
            to_address=booking.to_address,
            to_city=booking.to_city,
            to_state=booking.to_state,
            to_country=booking.to_country,
            to_pincode=booking.to_pincode,
            created_at=booking.created_at,
            updated_at=booking.updated_at,
            estimated_delivery_date=booking.estimated_delivery_date,
            estimated_delivery_cost=booking.estimated_delivery_cost,
            pickup_time=booking.pickup_time,
            pickup_date=booking.pickup_date,
        )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)

        # Add items if they exist
        if booking.booking_items:
            items_to_add = []
            for item in booking.booking_items:
                db_item = BookingItem(
                    booking_id=db_booking.booking_id,
                    weight=item.weight,
                    length=item.length,
                    width=item.width,
                    height=item.height,
                    package_type=item.package_type,
                    cost=item.cost,
                )
                items_to_add.append(db_item)
            db.add_all(items_to_add)
            db.commit()  # Commit after adding items

        return db_booking
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error occurred: {str(e)}")



def get_booking(db: Session, booking_id: int):
    return db.query(Bookings).filter(Bookings.booking_id == booking_id).first()


def get_all_bookings(db: Session, skip: int = 0, limit: int = 100,status: str = None):
    query = db.query(Bookings)
    if status:
        query = query.filter(Bookings.status == status)
    return query.offset(skip).limit(limit).all()


def update_booking(booking_id: int, booking_data: dict, db: Session):
    # Check if 'created_by' is a valid user
    created_by = booking_data.get('created_by')
    if created_by is None or not db.query(Users).filter(Users.user_id == created_by).first():
        raise HTTPException(status_code=400, detail="Invalid user_id for created_by")
    
    # Fetch the booking record
    booking = db.query(Bookings).filter(Bookings.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Update booking fields (excluding 'booking_items')
    for key, value in booking_data.items():
        if key != 'booking_items' and hasattr(booking, key) and value is not None:
            setattr(booking, key, value)

    # Update booking items if provided
    booking_items_data = booking_data.get('booking_items', [])
    if booking_items_data:
        for item_data in booking_items_data:
            item_id = item_data.get('item_id')
            if item_id:  # Update existing item
                booking_item = db.query(BookingItem).filter(BookingItem.item_id == item_id, BookingItem.booking_id == booking_id).first()
                if booking_item:
                    for key, value in item_data.items():
                        if hasattr(booking_item, key) and value is not None:
                            setattr(booking_item, key, value)
                else:
                    raise HTTPException(status_code=404, detail=f"Booking item with ID {item_id} not found")
            else:  # Add new item if no item_id is provided
                # Check if a similar item already exists (by matching item details)
                existing_item = db.query(BookingItem).filter(
                    BookingItem.booking_id == booking_id,
                    BookingItem.weight == item_data['weight'],
                    BookingItem.length == item_data['length'],
                    BookingItem.width == item_data['width'],
                    BookingItem.height == item_data['height'],
                    BookingItem.D_type == item_data['package_type']
                ).first()
                
                if existing_item:
                    raise HTTPException(status_code=400, detail="Duplicate booking item detected.")
                try:
                    new_item = BookingItem(**item_data, booking_id=booking_id)
                    db.add(new_item)
                except Exception as e:
                    raise HTTPException(status_code=400, detail=f"Error adding booking item: {str(e)}")
    
    # Commit the transaction
    db.commit()

    # Refresh the updated booking and return the response
    db.refresh(booking)
    return BookingDetailedResponse.from_orm(booking)





def delete_booking(db: Session, booking_id: int):
    db_booking = db.query(Bookings).filter(Bookings.booking_id == booking_id).first()
    if db_booking:
        db.delete(db_booking)
        db.commit()
        return {"message": "Booking deleted successfully"}
    return {"message": "Booking not found"}


# CRUD for Quotation
def create_quotation(db: Session, quotation: QuotationCreate):
    try:
        # Create booking record
        db_quotation = Quotations(
            user_id=quotation.user_id,
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
                    cost=item.cost,)
                items_to_add.append(db_item)
                db.add_all(items_to_add)
                db.commit()
        return db_quotation
    except Exception as e:
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=str(e))

def get_quotation(db: Session, quotation_id: int):
    return db.query(Quotations).filter(Quotations.quotation_id == quotation_id).first()


def get_all_quotations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Quotations).offset(skip).limit(limit).all()

def update_quotation(db: Session, quotation_id: int, quotation_data: dict):
    db_quotation = db.query(Quotations).filter(Quotations.quotation_id == quotation_id).first()

    if db_quotation:
        for key, value in quotation_data.items():
            if value is not None:
                setattr(db_quotation, key, value)
        db.commit()
        db.refresh(db_quotation)
        return db_quotation
    return None


def update_quotation_status(db: Session, quotation_id: int, status: str):
    db_quotation = db.query(Quotations).filter(Quotations.quotation_id == quotation_id).first()
    if db_quotation:
        db_quotation.status = status
        db.commit()
        db.refresh(db_quotation)
        return db_quotation
    return None


def delete_quotation(db: Session, quotation_id: int):
    db_quotation = db.query(Quotations).filter(Quotations.quotation_id == quotation_id).first()
    if db_quotation:
        db.delete(db_quotation)
        db.commit()
        return {"message": "Quotation deleted successfully"}
    return {"message": "Quotation not found"}


# CRUD for AddressBook
def create_address_book(db: Session, address: AddressBookCreate):
    db_address = AddressBook(
        user_id=address.user_id,
        name=address.name,
        address_line_1=address.address_line_1,
        address_line_2=address.address_line_2,
        city=address.city,
        state=address.state,
        postal_code=address.postal_code,
        country=address.country,
        mobile=address.mobile,
    )
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def get_address_book(db: Session, address_id: int):
    return db.query(AddressBook).filter(AddressBook.address_id == address_id).first()


def get_all_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AddressBook).offset(skip).limit(limit).all()


def update_address_book(db: Session, address_id: int, address_data: dict):
    db_address = db.query(AddressBook).filter(AddressBook.id == address_id).first()
    if db_address:
        for key, value in address_data.items():
            if value is not None:
                setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
        return db_address
    return None


def delete_address_book(db: Session, address_id: int):
    db_address = db.query(AddressBook).filter(AddressBook.address_id == address_id).first()
    if db_address:
        db.delete(db_address)
        db.commit()
        return {"message": "Address deleted successfully"}
    return {"message": "Address not found"}
