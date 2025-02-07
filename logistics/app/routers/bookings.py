from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session,joinedload
from app.schemas.bookings import ShippingRateRequest,ShippingRateResponse,BookingCreateRequeast, BookingListResponse
from app.databases.mysqldb import get_db
from app.service.bookings import create_booking_and_shipment_service, fetch_shipping_rates, cancel_booking_service, get_all_bookings_service,update_quotation_status_service
from typing import  List


router = APIRouter()

@router.post("/fetch-ups-rates/", response_model=List[ShippingRateResponse])
async def get_ups_shipping_rates(request_data: ShippingRateRequest):
    """
    API endpoint to fetch UPS shipping rates based on the given request data.
    This does NOT store data; it only retrieves shipping plans.
    """
    try:
       result = await fetch_shipping_rates(request_data.dict())  # Simulated function call

       # Check if result is None or contains an "error" key
       if not result or isinstance(result, dict) and "error" in result:
          raise HTTPException(status_code=400, detail=result)

       # Ensure the result contains the key 'shipping_rates' with a list value
       if 'shipping_rates' not in result:
          raise HTTPException(status_code=400, detail="Invalid response format, 'shipping_rates' not found.")
    
        # Map the result to include both shipper_address and ship_from_address
       shipping_rates = result['shipping_rates']
       for rate in shipping_rates:
        rate['shipper_address'] = request_data.ship_from_address  # Add ship_from_address as shipper_address
        rate['ship_from_address'] = request_data.ship_from_address  # Ensure ship_from_address is included in the response

       # Return the list of shipping rates
       return shipping_rates  # Now includes both 'shipper_address' and 'ship_from_address'
    except Exception as e:
        # General exception handling for unexpected errors
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create_booking/", response_model=ShippingRateResponse)
async def create_booking(request_data: BookingCreateRequeast, db: Session = Depends(get_db)):
    """
    Endpoint to create a booking and shipment using the UPS API.
    """
    try:
        # Pass both db and data as arguments to the service function
        response = create_booking_and_shipment_service(db, request_data.dict())
        
        # If there's an error in the service function, raise HTTPException
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])
        
        # Return the successful response
        return response
    except Exception as e:
        # General exception handling for unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/quotations/{quotation_id}/status")
async def update_quotation_status(quotation_id: str):
    """
    API endpoint to update the quotation status to 'Saved'.
    Calls the service layer for business logic.
    """
    try:
       response = await update_quotation_status_service(quotation_id)
       return response 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")   


@router.put("/cancelbookings/{booking_id}")
def cancel_booking(booking_id: int, db: Session = Depends(get_db)):
    """API endpoint to cancel a booking by booking_id."""
    try:
        cancelled_booking = cancel_booking_service(db, booking_id)
        return {"message": "Booking cancelled successfully", "booking_id": cancelled_booking.booking_id}
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/allbookingslist/", response_model=BookingListResponse)
def get_all_bookings(db: Session = Depends(get_db)):
    """API endpoint to fetch all bookings."""
    try:
        bookings = get_all_bookings_service(db)

        if not bookings:
            return {"bookings": [], "message": "No bookings found. Yet to create bookings."}

        return {"bookings": bookings, "message": "Bookings fetched successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bookings: {str(e)}")
