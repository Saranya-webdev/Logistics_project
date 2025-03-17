from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session,joinedload
from app.schemas.bookings import ShippingRateRequest,ShippingRateResponse,BookingCreateRequest, BookingListResponse,ShipmentCreateResponse
from app.databases.mysqldb import get_db
from app.service.bookings import create_booking_and_shipment_service, fetch_shipping_rates, cancel_booking_service, get_all_bookings_service,update_quotation_status_service
from typing import  List, Optional
from fastapi import Query


router = APIRouter()

@router.post("/fetch-ups-rates/", response_model=List[ShippingRateResponse])
async def get_ups_shipping_rates(request_data: ShippingRateRequest):
    """
    API endpoint to fetch UPS shipping rates based on the given request data.
    This does NOT store data; it only retrieves shipping plans.
    """
    try:
       result = await fetch_shipping_rates(request_data.dict())  

       if not result or isinstance(result, dict) and "error" in result:
          raise HTTPException(status_code=400, detail=result)

       if 'shipping_rates' not in result:
          raise HTTPException(status_code=400, detail="UPS API response does not contain 'shipping_rates'.")
       
       # Extract quotation_id from result
       quotation_id = result.get("quotation_id") 
    
        # Map the result to include both shipper_address and ship_from_address
       shipping_rates = result['shipping_rates']
       for rate in shipping_rates:
        rate['shipper_address'] = request_data.ship_from_address  
        rate['ship_from_address'] = request_data.ship_from_address 
        rate['quotation_id'] = quotation_id

        print("Final Shipping Rates:", shipping_rates)

       return shipping_rates  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create_booking/", response_model=ShipmentCreateResponse)
async def create_booking(request_data: BookingCreateRequest, db: Session = Depends(get_db)):
    try:
        print(f"Request Data: {request_data}")
        response = create_booking_and_shipment_service(db, request_data.dict())
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])
        return response
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
   

@router.put("/quotations/{quotation_id}/updatequotation")
async def update_quotation_status(quotation_id: str):
    """
    API endpoint to update the quotation status to 'Saved'.
    Calls the service layer for business logic.
    """
    try:
        response = await update_quotation_status_service(quotation_id)
        if "error" in response:
            raise HTTPException(status_code=400, detail=response["error"])
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
def get_all_bookings(booking_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """API endpoint to fetch all bookings."""
    try:
        bookings = get_all_bookings_service(db, booking_id)

        if not bookings:
            return {"bookings": [], "message": "No bookings found. Yet to create bookings."}

        return {"bookings": bookings, "message": "Bookings fetched successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching bookings: {str(e)}")
