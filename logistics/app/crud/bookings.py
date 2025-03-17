from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
import logging
from app.models.bookings import Bookings, BookingItem
from app.models.addressbooks import AddressBook
from app.databases.mongodb import quotations_collection
from bson import ObjectId
from typing import Optional


# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def save_quotation(data):
    """
    Save initial shipment details in MongoDB.
    """
    try:
        print(f"Saving quotation data: {data}")

        # Insert the quotation data into the quotations collection
        result = await quotations_collection.insert_one(data)
        
        # Fetch the inserted quotation ID from the result
        quotation_id = result.inserted_id 
        
        # `quotation_id` is the same as `_id`**
        await quotations_collection.update_one(
            {"_id": quotation_id},
            {"$set": {"quotation_id": quotation_id}} 
        )

        print(f"Quotation saved with ID: {quotation_id}") 
        
        # Return the result with the quotation ID
        return {"success": True, "quotation_id": str(quotation_id)}
    
    except Exception as e:
        print(f"Error saving quotation: {e}") 
        return {"success in saving quotation CRUD": False, "error in saving quotation CRUD": str(e)}

    

async def update_quotation(id, shipping_rates):
    """
    Update the quotation document with shipping rates using quotation_id.
    """
    try:
        if not ObjectId.is_valid(id):
            return {"success": False, "error in updating quotation CRUD": "Invalid quotation ID format."}

        quotation_object_id = ObjectId(id)

        # Find the quotation using `quotation_id`
        user_record = await quotations_collection.find_one({"quotation_id": quotation_object_id})

        if not user_record:
            return {"success": False, "error": "Quotation not found in the database."}

        result = await quotations_collection.update_one(
            {"quotation_id": quotation_object_id},
            {"$set": {"shipping_rates": shipping_rates, "status": "Unsaved"}}
        )

        if result.modified_count == 0:
            return {"success": False, "error in updating quotation CRUD": "No update performed on the quotation."}

        return {"success": True, "quotation_id": str(id), "message": "Quotation updated successfully"}

    except Exception as e:
        return {"success": False, "error in updating quotation CRUD": str(e)}


    

async def update_quotation_status_in_crud(quotation_id: str):
    try:
        if not ObjectId.is_valid(quotation_id):
            print(f"Invalid ObjectId: {quotation_id}")
            return {"success": False, "error in updating quotation status CRUD": "Invalid quotation ID format."}

        quotation_object_id = ObjectId(quotation_id)

        # Check if the quotation exists
        quotation_record = await quotations_collection.find_one({"quotation_id": quotation_object_id})

        if not quotation_record:
            return {"success": False, "error in updating quotation status CRUD": "Quotation not found."}

        # Update the status to 'Saved'
        result = await quotations_collection.update_one(
            {"quotation_id": quotation_object_id},
            {"$set": {"status": "Saved"}}
        )

        if result.modified_count == 0:
            print(f"No update performed for Quotation ID: {quotation_id}")
            return {"success": False, "error in updating quotation status CRUD": "No update performed on the quotation."}
        return {"success": True}

    except Exception as e:
        return {"success": False, "error": str(e)}




def create_booking_and_address_crud(db: Session, booking_data: dict):
    """
    CRUD function to create a booking and its related booking items.
    """
    try:
        # Convert customer_id to int
        customer_id = int(booking_data.get("customer_id", 0))
         
        print(f"booking data: {booking_data}")
        print(f"customer id: {customer_id}")

        # Create new booking
        tracking_number = booking_data.get("tracking_number")
        new_booking = Bookings(
            customer_id=customer_id,
            from_name=booking_data.get("ship_from_address", {}).get("from_name"),
            from_mobile=booking_data.get("ship_from_address", {}).get("from_mobile"),
            from_email=booking_data.get("ship_from_address", {}).get("from_email"),
            from_address=booking_data.get("ship_from_address", {}).get("from_address"),
            from_city=booking_data.get("ship_from_address", {}).get("from_city"),
            from_state=booking_data.get("ship_from_address", {}).get("from_state"),
            from_pincode=booking_data.get("ship_from_address", {}).get("from_pincode"),
            from_country=booking_data.get("ship_from_address", {}).get("from_country"),
            to_name = booking_data.get("ship_to_address", {}).get("to_name"),
            to_mobile=booking_data.get("ship_to_address", {}).get("to_mobile"),
            to_email=booking_data.get("ship_to_address", {}).get("to_email"),
            to_address=booking_data.get("ship_to_address", {}).get("to_address"),
            to_city=booking_data.get("ship_to_address", {}).get("to_city"),
            to_state=booking_data.get("ship_to_address", {}).get("to_state"),
            to_pincode=booking_data.get("ship_to_address", {}).get("to_pincode"),
            to_country=booking_data.get("ship_to_address", {}).get("to_country"),
            carrier_plan=booking_data.get("package_details", {}).get("carrier_plan"),
            carrier_name=booking_data.get("package_details", {}).get("carrier_name"),
            pickup_date=booking_data.get("pickup_date"),
            pickup_time=booking_data.get("pickup_time"),
            booking_status=booking_data.get("booking_status"),  # Initially set as Pending
            tracking_number=tracking_number if tracking_number else None,
            package_count=booking_data.get("package_details", {}).get("package_count"),
            est_cost=booking_data.get("package_details", {}).get("est_cost"),
            total_cost=booking_data.get("package_details", {}).get("total_cost"),
            est_delivery_date=booking_data.get("package_details", {}).get("est_delivery_date"),
            booking_date=booking_data.get("package_details", {}).get("booking_date"),
            booking_by=booking_data.get("package_details",{}).get("booking_by")

        )
        print(f"Before adding to DB: {new_booking.tracking_number}")
        print(f"new bookings: {new_booking}") 

        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)

        print(f"Booking created - Status: {new_booking.booking_status}, Tracking Number: {new_booking.tracking_number}")

        # Create booking items
        new_booking_items = []
        for item_data in booking_data.get("booking_items", []):
            new_item = BookingItem(
    booking_id=new_booking.booking_id,
    item_length=item_data.get("length"),
    item_width=item_data.get("width"),
    item_height=item_data.get("height"),
    item_weight=item_data.get("weight"),
    # volumetric_weight=item_data.get("volumetric_weight"),
    package_type=item_data.get("package_type"), 
    package_cost=item_data.get("package_cost")
)
            
            db.add(new_item)
            new_booking_items.append(new_item)
            db.commit()

        for item in new_booking_items:
            db.refresh(item)
        print(f"Booking created successfully with Pending status.")    
        return new_booking, new_booking_items
    except Exception as e:
        logger.error(f"Database error in create_booking_and_address_crud : {str(e)} | Booking Data in create_booking_and_address_crud: {booking_data}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error in create_booking_and_address_crud: {str(e)}")
    

def save_address_if_not_exists(db: Session, customer_id: int, booking: dict, is_from: bool):
    """
    Checks if the given address already exists for the customer in the addressbook.
    If not, inserts a new record.
    """
    address_prefix = "from_" if is_from else "to_"
    address_name = "from_address" if is_from else "to_address"

    # Extract address details
    address_data = {
        
        "address_name": address_name,
        "name": booking.get(f"ship_{address_prefix}address", {}).get(f"{address_prefix}name"),
        "mobile": booking.get(f"ship_{address_prefix}address", {}).get(f"{address_prefix}mobile"),
        "email_id": booking.get(f"ship_{address_prefix}address", {}).get(f"{address_prefix}email"),
        "address": booking.get(f"ship_{address_prefix}address", {}).get(f"{address_prefix}address"),
        "city": booking.get(f"ship_{address_prefix}address", {}).get(f"{address_prefix}city"),
        "state": booking.get(f"ship_{address_prefix}address", {}).get(f"{address_prefix}state"),
        "pincode": booking.get(f"ship_{address_prefix}address", {}).get(f"{address_prefix}pincode"),
        "country": booking.get(f"ship_{address_prefix}address", {}).get(f"{address_prefix}country"),
        "company_name": "", 
        "address_type": "Residential",
        "customer_id": customer_id
    }
    print(f"address data from crud:{address_data}")

    # Check if the address already exists
    existing_address = db.query(AddressBook).filter(
        AddressBook.customer_id == customer_id,
        AddressBook.address == address_data["address"],
        AddressBook.city == address_data["city"],
        AddressBook.state == address_data["state"],
        AddressBook.pincode == address_data["pincode"]
    ).first()

    if not existing_address:
        # Insert new address
        new_address = AddressBook(**address_data)
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        logger.info(f"New address saved: {new_address.address}")
    else:
        logger.info(f"Address already exists in the database: {existing_address.address}")    


def cancel_booking_status(db: Session, booking: Bookings):
    """Update the booking status in the database."""
    try:
        db.commit()
        db.refresh(booking)
        return booking
    except Exception as e:
        db.rollback()
        raise Exception(f"Database error while updating booking in cancel_booking_status CRUD: {e}")
    

def get_all_bookings_crud(db: Session, booking_id: Optional[int] = None):
    """Fetch all bookings from the database."""
    try:
        bookings = db.query(Bookings).options(
            joinedload(Bookings.booking_items)
        )
        if booking_id:
            bookings = bookings.filter(Bookings.booking_id == booking_id)
        bookings = bookings.all()

        for booking in bookings:
            # Convert pickup_time to a string format
            booking.pickup_time = booking.pickup_time.strftime("%H:%M:%S") if booking.pickup_time else None

            for item in booking.booking_items:
                # Check if it's a Non-Document package before validating dimensions/weight
                if item.package_type == "Non-Document":
                    if not all([
                        item.item_weight,  
                        item.item_length,  
                        item.item_width,   
                        item.item_height,  
                        item.package_cost
                    ]):
                        raise ValueError(f"BookingItem {item.item_id} has missing fields in get_all_bookings_crud.")
                
                # If it's a document, no need to check dimensions/weight
        return bookings

    except Exception as e:
        raise Exception(f"Database error while fetching bookings in get_all_bookings_crud: {e}")
