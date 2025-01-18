from sqlalchemy.orm import Session,joinedload
from app.schemas.bookings import BookingCreate, QuotationCreate, AddressBookCreate
from fastapi import HTTPException
import logging
from app.models.quotations import QuotationItems,Quotations
from app.models.bookings import Bookings, BookingItem
from app.models.addressbooks import AddressBook


# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Creates a new booking in the database.
def create_booking(db: Session, booking: BookingCreate):
    """
    Create a new booking in the database.
    """
    try:
        # Create the main booking object (no package_type here)
        db_booking = Bookings(
            customer_id=booking.customer_id,
            created_by=booking.created_by,
            pickup_method=booking.pickup_method,
            booking_status=booking.booking_status,
            name=booking.name,
            phone_number=booking.phone_number,
            email=booking.email,
            from_address=booking.from_address,
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
            estimated_delivery_cost=booking.estimated_delivery_cost,
            estimated_delivery_date=booking.estimated_delivery_date,
            package_count = booking.package_count,
            pickup_time=booking.pickup_time,
            pickup_date=booking.pickup_date,
            created_at=booking.created_at,
            updated_at=booking.updated_at, 
        )
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)

        # Add items to the BookingItem table, including package_type
        if booking.booking_items:
           items_to_add = []
           for item in booking.booking_items:
               db_item = BookingItem(
                   booking_id=db_booking.booking_id,
                   weight=item.weight,
                   length=item.length,
                   width=item.width,
                   height=item.height,
                   package_type=item.package_type,  # Correct place for package_type
                   cost=item.cost,
               )
               items_to_add.append(db_item)
           db.add_all(items_to_add)
           db.commit()

        return db_booking
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating a booking: {str(e)}")
        raise



# Fetches a booking by ID.
def get_booking(db: Session, booking_id: int):
    """
    Retrieve a booking by their ID.
    """
    try:
        booking = db.query(Bookings).filter(Bookings.booking_id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return booking
    except Exception as e:
        logger.error(f"Error fetching booking with ID {booking_id}: {str(e)}")
        raise

# Fetches all bookings from the database.
def get_all_bookings(db: Session):
    """
    Retrieve all bookings from the database with their quotation details.
    """
    try:
       return db.query(Bookings).options(joinedload(Bookings.quotation)).all()
    except Exception as e:
        logger.error(f"Error fetching all bookings: {str(e)}")
        raise

# Updates a booking by ID.
def update_booking(db: Session, booking_id: int, update_data: dict):
    """
    update an existing booking in the database.
    """
    existing_booking = db.query(Bookings).filter(Bookings.booking_id == booking_id).first()
    if not existing_booking:
        return None

    booking_items_data = update_data.pop('booking_items', None)

    for key, value in update_data.items():
        setattr(existing_booking, key, value)

    if booking_items_data is not None:
        for item_data in booking_items_data:
            if isinstance(item_data, dict):
                item_instance = BookingItem(**item_data)
            else:
                item_instance = item_data

            existing_item = db.query(BookingItem).filter(BookingItem.item_id == item_instance.item_id).first()
            if existing_item:
                for key, value in item_data.items():
                    setattr(existing_item, key, value)
            else:
                item_instance.booking_id = booking_id  # Set the booking_id for new items
                existing_booking.booking_items.append(item_instance)

    db.commit()
    db.refresh(existing_booking)

    # Add booking_id to each booking_item for response
    for item in existing_booking.booking_items:
        item.booking_id = existing_booking.booking_id

    return existing_booking


# Deletes a booking by ID.
def delete_booking(db: Session, booking_id: int):
    """
    Delete a booking by their ID.
    """
    try:
       booking_to_delete = db.query(Bookings).filter(Bookings.booking_id == booking_id).first()
       if not booking_to_delete:
        raise HTTPException(status_code=404, detail="Booking ID not found")
       
       db.delete(booking_to_delete)
       db.commit()
       return {"detail": f"Booking {booking_to_delete.name} (ID: {booking_to_delete.booking_id}) deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting booking with ID {booking_id}: {str(e)}")
        raise

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


# Creates a new address book in the database.
def create_address_book(db: Session, address: AddressBookCreate):
    """
    Create a new address book in the database.
    """
    try:
        db_address = AddressBook(
        customer_id=address.customer_id,
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
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating address book: {str(e)}")
        raise

# Fetches an address book by ID.
def get_address_book(db: Session, address_id: int):
    """
    Retrieve an addressbook by their ID.
    """
    try:
        address_book = db.query(AddressBook).filter(AddressBook.address_id == address_id).first()
        if not address_book:
            raise HTTPException(status_code=404, detail="address book not found")
        return address_book
    except Exception as e:
        logger.error(f"Error fetching address book with ID {address_id}: {str(e)}")
        raise

# Fetches all address book from the database.
def get_all_addresses(db: Session):
    """
    Retrieve all address book from the database.
    """
    try:
        return db.query(AddressBook).all()
    except Exception as e:
        logger.error(f"Error fetching all address books: {str(e)}")
        raise

# Updates a address_book by ID.
def update_address_book(db: Session, address_id: int, address_data: dict):
    """
    Update an existing address book by their ID.
    """
    try:
       db_address = db.query(AddressBook).filter(AddressBook.address_id == address_id).first()

       if db_address:
        for key, value in address_data.items():
            if value is not None:
                setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
        return db_address
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating address book with ID {address_id}: {str(e)}")
        raise

# Deletes a address by ID.
def delete_address_book(db: Session, address_id: int):
    """
    Delete an address book by their ID.
    """
    try:
       addressbook_to_delete = db.query(AddressBook).filter(AddressBook.address_id == address_id).first()
       if addressbook_to_delete:
            db.delete(addressbook_to_delete)
            db.commit()
            return {"detail": f"Address {addressbook_to_delete.address_id} deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting address book with ID {address_id}: {str(e)}")
        raise

    
