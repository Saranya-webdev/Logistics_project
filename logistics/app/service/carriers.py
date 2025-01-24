from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.carriers import Carrier
from app.models.bookings import Bookings
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.utils import check_existing_carrier_by_mobile
import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

def create_carrier_service(db: Session, carrier_data: dict) -> dict:
    """
    Business logic for creating an carrier.
    """
    try:
        # Log validation process
        logger.info("Validating if the carrier already exists...")

        # Check if carrier already exists using mobile number
        if check_existing_carrier_by_mobile(db, carrier_data["carrier_mobile"]):
            return {"message": "carrier already exists"}

        # Set default values
        carrier_data["active_flag"] = 1  # Default active_flag to 0

        logger.info("Creating new carrier...")
        # Create the new carrier
        new_carrier = carrier(**carrier_data)
        db.add(new_carrier)
        db.commit()
        db.refresh(new_carrier)

        # Return the created carrier details
        return {
            "message": "carrier created successfully",
            "carrier_id": new_carrier.carrier_id,
            "carrier_name": new_carrier.carrier_name,
            "carrier_mobile": new_carrier.carrier_mobile,
            **{key: getattr(new_carrier, key) for key in carrier_data.keys()}
            
        }

    except IntegrityError as e:
        logger.error(f"IntegrityError: {str(e)}")
        db.rollback()
        return {"message": "Database error occurred. Please check input data."}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        db.rollback()
        return {"message": f"Error creating carrier: {str(e)}"}

def update_carrier_service(db: Session, carrier_data: dict) -> dict:
    """Business logic for updating an carrier's details based on carrier email."""
    try:
        # Step 1: Check if the carrier exists based on email
        existing_carrier = db.query(Carrier).filter(Carrier.carrier_email == carrier_data["carrier_email"]).first()
        if not existing_carrier:
            return {"message": "No carriers found"}  # Return message if no carrier is found

        # Step 2: Exclude fields that shouldn't be updated (verification_status, category, notes)
        fields_to_exclude = ["verification_status", "carrier_category", "notes"]
        filtered_data = {key: value for key, value in carrier_data.items() if key not in fields_to_exclude and value is not None}

        # Step 3: Update carrier details with the filtered data
        for field, value in filtered_data.items():
            if hasattr(existing_carrier, field):
                setattr(existing_carrier, field, value)

        # Commit changes to the database
        db.commit()
        db.refresh(existing_carrier)

        # Return the updated carrier details
        return {
            "carrier_id": existing_carrier.carrier_id,
            "carrier_name": existing_carrier.carrier_name,
            "carrier_email": existing_carrier.carrier_email,
            "carrier_mobile": existing_carrier.carrier_mobile,
            "carrier_address": existing_carrier.carrier_address,
            "carrier_city": existing_carrier.carrier_city,
            "carrier_state": existing_carrier.carrier_state,
            "carrier_country": existing_carrier.carrier_country,
            "carrier_pincode": existing_carrier.carrier_pincode,
            "carrier_geolocation": existing_carrier.carrier_geolocation,
            "carrier_businessname": existing_carrier.carrier_businessname,
            "tax_id": existing_carrier.tax_id,
            "active_flag": existing_carrier.active_flag,
        }

    except IntegrityError as e:
        db.rollback()
        return {"message": f"Database error: {str(e)}"}
    except Exception as e:
        db.rollback()
        return {"message": f"Error updating carrier: {str(e)}"}



def suspend_or_activate_carrier(db: Session, carrier_mobile: str, active_flag: int, remarks: str) -> dict:
    """
    Suspend or activate an carrier based on the active_flag input.

    Args:
        db (Session): Database session.
        carrier_mobile (str): Mobile number of the carrier.
        active_flag (int): 1 for activate, 2 for suspend.
        remarks (str): Remarks or notes for the action.

    Returns:
        dict: Updated carrier details or error message.
    """
    from app.crud.carriers import get_carrier_by_mobile, update_carrier_status
    try:
        # Step 1: Validate the active flag value
        if active_flag not in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid active flag value. Use 1 (Activate) or 2 (Suspend)."
            )

        # Step 2: Fetch the carrier by mobile
        existing_carrier = get_carrier_by_mobile(db, carrier_mobile)
        if not existing_carrier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No carrier found with the provided mobile number."
            )

        # Step 3: Update the carrier's status
        update_carrier_status(db, existing_carrier, active_flag, remarks)
        db.refresh(existing_carrier)

        # Step 4: Return the updated carrier details
        return {
            'message': 'carrier status updated successfully.',
            "carrier": {
                "carrier_id": existing_carrier.carrier_id,
                "carrier_name": existing_carrier.carrier_name,
                "carrier_email": existing_carrier.carrier_email,
                "carrier_mobile": existing_carrier.carrier_mobile,
                "carrier_address": existing_carrier.carrier_address,
                "carrier_city": existing_carrier.carrier_city,
                "carrier_state": existing_carrier.carrier_state,
                "carrier_country": existing_carrier.carrier_country,
                "carrier_pincode": existing_carrier.carrier_pincode,
                "carrier_geolocation": existing_carrier.carrier_geolocation,
                "carrier_category": existing_carrier.carrier_category.value,
                "carrier_businessname": existing_carrier.carrier_businessname,
                "tax_id": existing_carrier.tax_id,
                "active": active_flag == 1,
                "verification_status": existing_carrier.verification_status,
                "remarks": existing_carrier.remarks
            }
        }
    

    except HTTPException as http_exc:
        # Re-raise HTTP exceptions
        raise http_exc
    except Exception as e:
        # Rollback the transaction on error
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating carrier status: {str(e)}"
        )

def verify_carrier_service(db: Session, carrier_mobile: str, verification_status: str) -> dict:
    """
    Verify the carrier and update their verification status and active flag.

    Args:
        db (Session): Database session.
        carrier_mobile (str): Mobile number of the carrier.
        verification_status (str): Verification status ('Verified' or 'Not Verified').

    Returns:
        dict: Updated carrier details or error message.
    """
    try:
        # Step 1: Retrieve the carrier based on the mobile number
        existing_carrier = db.query(Carrier).filter(Carrier.carrier_mobile == carrier_mobile).first()

        if not existing_carrier:
            # Step 2: Return message if the carrier is not found
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No carrier found with the provided mobile number."
            )

        # Step 3: Update verification status and active flag
        if verification_status.lower() == "verified":
            existing_carrier.verification_status = "Verified"
            existing_carrier.active_flag = 1  # Activate the carrier
        else:
            existing_carrier.verification_status = verification_status
            existing_carrier.active_flag = 0  # Optional: Deactivate or leave unchanged

        # Commit the changes to the database
        db.commit()
        db.refresh(existing_carrier)

        # Step 4: Return the updated carrier details
        return {
            "message": "carrier verification status updated successfully.",
            "carrier": {
                "carrier_id": existing_carrier.carrier_id,
                "carrier_name": existing_carrier.carrier_name,
                "carrier_email": existing_carrier.carrier_email,
                "carrier_mobile": existing_carrier.carrier_mobile,
                "carrier_address": existing_carrier.carrier_address,
                "carrier_city": existing_carrier.carrier_city,
                "carrier_state": existing_carrier.carrier_state,
                "carrier_country": existing_carrier.carrier_country,
                "carrier_pincode": existing_carrier.carrier_pincode,
                "carrier_geolocation": existing_carrier.carrier_geolocation,
                "carrier_businessname": existing_carrier.carrier_businessname,
                "tax_id": existing_carrier.tax_id,
                "verification_status": existing_carrier.verification_status,
                "active_flag": existing_carrier.active_flag,
            },
        }
    except Exception as e:
        # Rollback the transaction in case of an unexpected error
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying carrier: {str(e)}"
        )


def get_carrier_profile(db: Session, carrier_mobile: str) -> dict:
    """Retrieve the profile of an carrier based on their mobile number."""
    from app.crud.carriers import get_carrier_by_mobile
    carrier = get_carrier_by_mobile(db, carrier_mobile)
    if not carrier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="carrier not found")

    response = {
        "carrier_id": carrier.carrier_id,
        "carrier_name": carrier.carrier_name,
        "carrier_email": carrier.carrier_email,
        "carrier_mobile": carrier.carrier_mobile,
        "carrier_address": carrier.carrier_address,
        "carrier_city": carrier.carrier_city,
        "carrier_state": carrier.carrier_state,
        "carrier_country": carrier.carrier_country,
        "carrier_pincode": carrier.carrier_pincode,
        "carrier_geolocation": carrier.carrier_geolocation,
        "carrier_businessname": carrier.carrier_businessname,
        "tax_id": carrier.tax_id,
        "verification_status": carrier.verification_status,
    }
    return response


def get_all_carriers_with_booking_list(db: Session) -> list:
    """
    Retrieve all carriers with their booking list summaries.
    """
    try:
        carriers = db.query(carrier).all()
        if not carriers:
            raise HTTPException(status_code=404, detail="No carriers found")

        carrier_list = []
        for carrier in carriers:
            bookings = db.query(Bookings).filter(Bookings.carrier_id == carrier.carrier_id).all()
            booking_summary = [
                {
                    "booking_id": booking.booking_id,
                    "from_city": booking.from_city,
                    "from_pincode": booking.from_pincode,
                    "to_city": booking.to_city,
                    "to_pincode": booking.to_pincode,
                    "status": booking.booking_status,
                    "action": f"View details of Booking {booking.booking_id}",
                }
                for booking in bookings
            ]
            response = {
                "carrier_id": carrier.carrier_id,
                "carrier_name": carrier.carrier_name,
                "carrier_mobile": carrier.carrier_mobile,
                "carrier_email": carrier.carrier_email,
                "carrier_address": carrier.carrier_address,
                "carrier_city": carrier.carrier_city,
                "carrier_state": carrier.carrier_state,
                "carrier_country": carrier.carrier_country,
                "carrier_pincode": carrier.carrier_pincode,
                "carrier_geolocation": carrier.carrier_geolocation,
                "carrier_businessname": carrier.carrier_businessname,
                "tax_id": carrier.tax_id,
                "verification_status": carrier.verification_status,
                "active_flag": carrier.active_flag,
                "carrier_category": carrier.carrier_category,
                "bookings": booking_summary
            }
            carrier_list.append(response)

        return carrier_list

    except Exception as e:
        logging.error(f"Error fetching carrier list with booking summaries: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching carrier list: {str(e)}")



def get_carrier_with_booking_details(db: Session, carrier_id: int, booking_id: int):
    from app.models.bookings import BookingItem  # Import BookingItem
    try:
        # Query the booking with the specified carrier_id and booking_id
        booking = db.query(Bookings).filter(Bookings.carrier_id == carrier_id, Bookings.booking_id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        # Retrieve the carrier details
        carrier = db.query(carrier).filter(carrier.carrier_id == carrier_id).first()
        if not carrier:
            raise HTTPException(status_code=404, detail="carrier not found")


        # Prepare the booking response with carriers and booking details
        booking_response = {
            "carrier_name": carrier.carrier_name,
            "carrier_mobile": carrier.carrier_mobile,
            "carrier_email": carrier.carrier_email,
            "carrier_address": carrier.carrier_address,
            "carrier_city": carrier.carrier_city,
            "carrier_state": carrier.carrier_state,
            "carrier_country": carrier.carrier_country,
            "carrier_pincode": carrier.carrier_pincode,
            "booking_id": booking.booking_id,
            "from_address": booking.from_address,
            "from_city": booking.from_city,
            "from_pincode": booking.from_pincode,
            "to_address": booking.to_address,
            "to_city": booking.to_city,
            "to_pincode": booking.to_pincode,
            "package_details": {
                "no_of_packages": booking.package_count,
                "pickup_date": booking.pickup_date,
                "pickup_time": booking.pickup_time,
                "estimated_delivery_date": booking.estimated_delivery_date
            },
            "item_details": [
                {
                    "item_id": item.item_id,
                    "booking_id": item.booking_id,
                    "weight": item.weight,
                    "length": item.length,
                    "width": item.width,
                    "height": item.height,
                    "package_type": item.package_type.name,  # Assuming package_type is an enum
                    "cost": item.cost,
                    "ratings": item.rating,
                }
                for item in db.query(BookingItem).filter(BookingItem.booking_id == booking.booking_id).all()
            ],
        }

        return booking_response

    except Exception as e:
        logging.error(f"Error retrieving booking details for carrier {carrier_id} and booking {booking_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def get_carrier_booking_list(carrier_id: int, db: Session):
    from app.crud.carriers import get_carriers_and_bookings
    from app.schemas.carriers import carrierBookingListResponse
    from app.schemas.bookings import BookingSummary

    try:
        # Fetch carrier and bookings
        carrier, bookings = get_carriers_and_bookings(db, carrier_id)

        if not carrier:
            raise HTTPException(status_code=404, detail="carrier not found")

        # Construct booking summary
        booking_summary = [
            BookingSummary(
                booking_id=booking.booking_id,
                from_city=booking.from_city,
                from_pincode=booking.from_pincode,
                to_city=booking.to_city,
                to_pincode=booking.to_pincode,
                status=booking.booking_status,
                action=f"View details of Booking {booking.booking_id}",
            )
            for booking in bookings
        ]

        # Construct response
        return carrierBookingListResponse(
            carrier_id=carrier.carrier_id,
            carrier_name=carrier.carrier_name,
            carrier_mobile=carrier.carrier_mobile,
            carrier_email=carrier.carrier_email,  # Ensure this matches the schema
            carrier_address=carrier.carrier_address,
            carrier_city=carrier.carrier_city,
            carrier_state=carrier.carrier_state,
            carrier_country=carrier.carrier_country,
            carrier_pincode=carrier.carrier_pincode,
            carrier_geolocation=carrier.carrier_geolocation,
            tax_id=carrier.tax_id,
            carrier_businessname=carrier.carrier_businessname,
            bookings=booking_summary,
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error fetching carrier booking list: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching booking list: {str(e)}")
