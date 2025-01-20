from sqlalchemy.orm import Session,joinedload
from app.schemas.bookings import BookingCreate,BookingDetailedResponse
from fastapi import HTTPException
import logging
from app.models.bookings import Bookings, BookingItem
from app.models.enums import PickupMethod, RatingEnum

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Creates a new booking in the database.
def create_booking(db: Session, booking: BookingCreate):
    """
    Create a new booking in the database.
    """
    try:
        # From Details
        from_details = {
            "customer_id": booking.customer_id,
            "created_by": booking.created_by,
            "name": booking.name,
            "phone_number": booking.phone_number,
            "email": booking.email,
            "from_address": booking.from_address,
            "city": booking.city,
            "state": booking.state,
            "country": booking.country,
            "pincode": booking.pincode
        }

        # To Details
        to_details = {
            "to_name": booking.to_name,
            "to_phone_number": booking.to_phone_number,
            "to_email": booking.to_email,
            "to_address": booking.to_address,
            "to_city": booking.to_city,
            "to_state": booking.to_state,
            "to_country": booking.to_country,
            "to_pincode": booking.to_pincode
        }

        # Pickup Details
        pickup_details = {
            "pickup_method": booking.booking_items[0].pickup_method,  # Assuming uniform pickup method for all items
            "pickup_time": booking.booking_items[0].pickup_time,
            "pickup_date": booking.booking_items[0].pickup_date
        }

        # Create the main booking object
        db_booking = Bookings(
    **from_details,
    **to_details,
    **pickup_details,  # pickup_time is already included here
    package_count=len(booking.booking_items),
    booking_status=booking.booking_items[0].booking_status,
    estimated_delivery_cost=booking.estimated_delivery_cost,
    estimated_delivery_date=booking.estimated_delivery_date, 
    created_at=booking.created_at,
    updated_at=booking.updated_at
)


        # Add the main booking to the database
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)

        # Item Details
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
        rating=RatingEnum.one
        )
        items_to_add.append(db_item)
        db.add_all(items_to_add)
        db.commit()

        return db_booking
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating a booking: {str(e)}")
        raise Exception(f"Error creating a booking: {str(e)}")


# Fetches a booking by ID.
def get_booking(db: Session, booking_id: int):
    """
    Retrieve a booking by their ID.
    """
    try:
        booking = db.query(Bookings).options(joinedload(Bookings.booking_items)).filter(Bookings.booking_id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        # Ensure that all booking items have a pickup_method
        for item in booking.booking_items:
            if not item.pickup_method:
                item.pickup_method = PickupMethod.user_address  # You can choose an appropriate default

        return booking
    except Exception as e:
        logger.error(f"Error fetching booking with ID {booking_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Fetches all bookings from the database.
def get_all_bookings(db: Session):
    """
    Retrieve all bookings from the database with their quotation details.
    """
    try:
        # Query the required fields, joining the necessary tables
        bookings = db.query(
            Bookings.booking_id,
            Bookings.from_address,
            Bookings.city.label("from_city"),
            Bookings.pincode.label("from_pincode"),
            Bookings.to_address,
            Bookings.to_city,
            Bookings.to_pincode,
            BookingItem.package_type,
            Bookings.booking_status,
            Bookings.payment_status,  # Use payment_status
            BookingItem.rating  # Assuming 'rating' exists in BookingItem
        ).join(BookingItem, Bookings.booking_id == BookingItem.booking_id, isouter=True).all()  # Outer join to handle cases with no rating

        # Map the query results to the custom response model
        booking_summaries = [
            BookingDetailedResponse(
                booking_id=booking.booking_id,
                from_address=booking.from_address,
                from_city=booking.from_city,
                from_pincode=booking.from_pincode,
                to_address=booking.to_address,
                to_city=booking.to_city,
                to_pincode=booking.to_pincode,
                package_type=booking.package_type.name if booking.package_type else None,  # Ensure no NoneType
                booking_status=booking.booking_status,
                payment_status=booking.payment_status.lower() if booking.payment_status else "unknown",  # Normalize to lowercase
                rating=booking.rating if booking.rating is not None else "Not Rated"  # Handle missing ratings
            )
            for booking in bookings
        ]

        return booking_summaries

    except Exception as e:
        logger.error(f"Error fetching all bookings: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching bookings")


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


    
