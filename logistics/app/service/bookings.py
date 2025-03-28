from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.customers import Customer
from app.models.bookings import Bookings
from app.utils.ups_utils import ups_create_shipment, get_ups_shipping_rates, ups_get_access_token
import logging
from app.crud.bookings import create_booking_and_address_crud, get_all_bookings_crud,cancel_booking_status,save_address_if_not_exists,update_quotation,save_quotation, update_quotation_status_in_crud
from app.crud.addressbook import get_all_addresses
from bson import ObjectId
from datetime import datetime
import json
from typing import Optional



logger = logging.getLogger(__name__)

# Business logics for fetch shipping rates and save to quotation collection
async def fetch_shipping_rates(data: dict):
    try:
        client_id = "7WSnxKncCMa5mhBZIPwMv5zxnhXRsNTIt5z6IwsicieNrdG2"
        client_secret = "uENQxqH6pWWhxUTIf8iQy8jJlLXBxTaJhRZ9qiGP7VPoqB0qAYgI8ctPtpeEzw53"
        access_token = ups_get_access_token(client_id, client_secret)

        if not access_token:
            return {"error": "Failed to retrieve UPS access token."}

        package_data = data.get("package_details", [{}])[0]

        pickup_date = data.get("pickup_date", "")  
        pickup_time = data.get("pickup_time", "") 
        print(f"Sending to UPS API: pickup_date={pickup_date}, pickup_time={pickup_time}")

        package_count = int(data.get("package_count", 0))  

        if not package_data:
            return {"error": "Missing 'package_details' in request"}

        # Validate required fields
        package_type = package_data.get("package_type")
        if not package_type:
            return {"error": "Missing 'package_type' in package_details"}

        # Assign package attributes based on package_type_code
        if package_type == "Document":  # Document package type
            package_data["packagebilltype"] = "02"
            package_data["DocumentsOnlyIndicator"] = "Document"
            package_data["PackagingType"] = {"Code": "01"}  # UPS Letter
        else:  # Non-Document package type
            package_data["packagebilltype"] = "03"
            # package_data["DocumentsOnlyIndicator"] = "Non-Document"
            package_data["PackagingType"] = {"Code": "02"}  # Other Packaging

        # Extract user details
        user_email = data.get("UserEmail", "")

        # Set shipper and recipient addresses
        shipper_address = { 
            "Name": "Thisai", 
            "AddressLine": ["1834 Blazewood Street"],
            "City": "Simi Valley",
            "StateProvinceCode": "CA",
            "PostalCode": "93063",
            "CountryCode": "US"
        }
        ship_to_address = {
            "name": data.get("ship_to_address", {}).get("Name", ""),
            # "address_line_1": data.get("ship_to_address", {}).get("AddressLine", ""),
            # "address_line_2":data.get("ship_to_address", {}).get("AddressLine", ""),
            # "address_line_3":data.get("ship_to_address", {}).get("AddressLine", ""),
            "Address": data.get("ship_to_address", {}).get("Address", ""),
            "Mobile": data.get("ship_to_address", {}).get("Mobile", ""),
            "Email": data.get("ship_to_address",{}).get("Email",""),
            "city": data.get("ship_to_address", {}).get("City", ""),
            "stateprovince": data.get("ship_to_address", {}).get("StateProvinceCode", ""),
            "postal_code": data.get("ship_to_address", {}).get("PostalCode", ""),
            "country_code": data.get("ship_to_address", {}).get("CountryCode", "")
        }
        ship_from_address = {
            "name": data.get("ship_from_address", {}).get("Name", ""),
            # "address_line_1": data.get("ship_from_address", {}).get("AddressLine", ""),
            # "address_line_2":data.get("ship_from_address", {}).get("AddressLine", ""),
            # "address_line_3":data.get("ship_from_address", {}).get("AddressLine", ""),
            "Address": data.get("ship_from_address", {}).get("Address", ""),
            "Mobile": data.get("ship_from_address", {}).get("Mobile", ""),
            "Email": data.get("ship_from_address",{}).get("Email",""),
            "city": data.get("ship_from_address", {}).get("City", ""),
           "stateprovince": data.get("ship_from_address", {}).get("StateProvinceCode", ""),
           "postal_code": data.get("ship_from_address", {}).get("PostalCode", ""),
           "country_code": data.get("ship_from_address", {}).get("CountryCode", "")
        }
        package_details = {
            "Packaging": {
                "Code": package_data.get("PackagingType", {}).get("Code", ""),
                "Description": "Nails"
            },
            "DeliveryTimeInformation": {
                "PackageBillType": package_data.get("packagebilltype", ""),
                "Pickup": {"Date": pickup_date, "Time": pickup_time}
            },
            "NumOfPieces": package_count,
            "DocumentsOnlyIndicator": package_data.get("DocumentsOnlyIndicator", ""),
            "Dimensions": {
                "UnitOfMeasurement": {"Code": "IN", "Description": "Inches"},
                "Length": package_data.get("length", ""),
                "Width": package_data.get("width", ""),
                "Height": package_data.get("height", "")
            },
            "PackageWeight": {
                "UnitOfMeasurement": {"Code": "LBS", "Description": "Pounds"},
                "Weight": float(package_data.get("weight", 0)) 

            },
        }
        print(f"Sending to UPS API: pickup_date={pickup_date}, pickup_time={pickup_time}")

        print(f"Pickup date from service: {pickup_date}")
        print(f"Package count from service: {package_count}")
        print(f"Package Weight from service: {package_details.get('PackageWeight', {}).get('Weight')}")

        # Prepare the quotation data directly
        quotation_data = {
            "quotation_id": ObjectId(),
            "address":{
            "ship_to": ship_to_address,
            "ship_from": ship_from_address,
            },
            
            "package_details": package_details,
            "status": "unsaved",
            # "created_by": {
            #     "usertype": data.get("UserType", "") if data.get("UserType") else None,
            #     "userid": data.get("UserId","") if data.get("UserId") else None,
            # }
        }
        print(f"package details from service: {package_details}")

        # Save the initial quotation to DB
        quotation_result = await save_quotation(quotation_data)
        quotation_id = quotation_result.get("quotation_id")
        print(f"Quotation saved with ID: {quotation_id}")

        if not quotation_result.get("success"):
            return {"error": "Failed to store quotation in database."}
    
        # Call UPS API to get rates
        shipping_rates_response = await get_ups_shipping_rates(
            access_token,
            shipper_address,
            ship_to_address, 
            ship_from_address,
            package_details,
            pickup_date,
            pickup_time,
            package_count
        )

        if not shipping_rates_response:
            return {"error": "Failed to retrieve shipping rates from UPS."}

        # Process UPS rates and update quotation
        processed_shipping_rates = []
        for rate in shipping_rates_response:
            processed_shipping_rates.append({
                "service_code": rate.get("service_code", ""),
                "service_desc": rate.get("service_desc", ""),
                "service_name": rate.get("service_name", ""),
                "transit_time": rate.get("transit_time", ""),
                "estimated_arrival_date": rate.get("estimated_arrival_date", ""),
                "estimated_arrival_time": rate.get("estimated_arrival_time", ""),
                "dayofweek": rate.get("dayofweek", ""),
                "total_charges": float(rate.get("total_charges", 0))
            })
        # Update the quotation with shipping rates
        update_result = await update_quotation(quotation_id, processed_shipping_rates)

        if not update_result.get("success"):
            return {"error": "Failed to update quotation with shipping rates."}

        return {"success": True,
                "quotation_id": quotation_result.get("quotation_id"),
                  "shipping_rates": processed_shipping_rates}

    except Exception as e:
        return {"error": str(e)}
    
    

# Business logics for update the quotation status in quotation collection(MongoDb)
async def update_quotation_status_service(quotation_id: str):
    """
    Business logic for updating the quotation status.
    Ensures the status is updated to 'Saved' and returns an appropriate response.
    """
    try:
        # Call the database function
        update_result = await update_quotation_status_in_crud(quotation_id)

        if not update_result.get("success"):
            return {"error": update_result.get("error")}

        return {"message": "Quotation saved successfully"}

    except Exception as e:
        return {"error": str(e)}
    
    
# Business logics for create a booking and shipment service(in Mysql DB)
def create_booking_and_shipment_service(db: Session, booking_data: dict) -> dict:
    """
    Service function to create a booking and a shipment, ensuring that:
    1. Customer existence is validated.
    2. Booking details are created in the booking table.
    3. Shipment is created by calling UPS API.
    4. Relevant data is returned.
    """
    try:
        # Normalize keys to lowercase in booking_data
        booking_data = {key.lower(): value for key, value in booking_data.items()}

        # Check if customer exists
        customer_id = booking_data.get("customer_id")
        customer_exists = db.query(Customer).filter(Customer.customer_id == customer_id).first()

        if not customer_exists:
            return {"error": f"Customer ID {customer_id} does not exist."}

        # Create booking and associated booking items
        new_booking, new_booking_items = create_booking_and_address_crud(db, booking_data)
        logger.info(f"New booking: {new_booking}")
        logger.info(f"Booking items: {new_booking_items}")

        # Save 'from' and 'to' addresses if they don't already exist
        save_address_if_not_exists(db, customer_id, booking_data, is_from=True)
        save_address_if_not_exists(db, customer_id, booking_data, is_from=False)


        # Prepare response data for the booking creation
        booking_response_data = {
            "customer_id": new_booking.customer_id,
            "booking_id": new_booking.booking_id,
            "from_name": new_booking.from_name,
            "from_mobile": new_booking.from_mobile,
            "from_address": new_booking.from_address,
            "from_email": new_booking.from_email,
            "from_city": new_booking.from_city,
            "from_state": new_booking.from_state,
            "from_pincode": new_booking.from_pincode,
            "from_country": new_booking.from_country,
            "to_name": new_booking.to_name,
            "to_mobile": new_booking.to_mobile,
            "to_email": new_booking.to_email,
            "to_address": new_booking.to_address,
            "to_city": new_booking.to_city,
            "to_state": new_booking.to_state,
            "to_pincode": new_booking.to_pincode,
            "to_country": new_booking.to_country,
            "carrier_name": new_booking.carrier_name,
            "carrier_plan": new_booking.carrier_plan,
            "est_cost": new_booking.est_cost,
            "est_delivery_date": new_booking.est_delivery_date,
            "pickup_date": new_booking.pickup_date,
            "pickup_time": new_booking.pickup_time,
            "total_cost": new_booking.total_cost,
            "booking_date": new_booking.booking_date,
            "booking_by":new_booking.booking_by,
            "package_count": new_booking.package_count,
            "booking_status": new_booking.booking_status,
            "tracking_number": new_booking.tracking_number,
            "booking_items": [
                {
                    "length": item.item_length,
                    "weight": item.item_weight,
                    "width": item.item_width,
                    "height": item.item_height,
                    "package_type": item.package_type,
                    "package_cost": item.package_cost,
                } for item in new_booking_items
            ] if new_booking_items else []
        }
        logger.info(f"Pickup Date: {booking_data.get('booking_status')}")
        logger.info(f"Pickup Date: {booking_data.get('tracking_number')}")

        logger.info(f"Booking response data: {booking_response_data}")
        logger.info(f"Pickup Date: {booking_data.get('pickup_date')}")
        logger.info(f"Pickup Time: {booking_data.get('pickup_time')}")

        # UPS shipment creation (this is the only step where shipment_data is used)
        # Load UPS credentials
        client_id = "7WSnxKncCMa5mhBZIPwMv5zxnhXRsNTIt5z6IwsicieNrdG2"
        client_secret = "uENQxqH6pWWhxUTIf8iQy8jJlLXBxTaJhRZ9qiGP7VPoqB0qAYgI8ctPtpeEzw53"
        access_token = ups_get_access_token(client_id, client_secret)

        # Define static shipper address details
        shipper_address = {
            "Name": "Thisai",
            "AddressLine": ["1834 Blazewood Street"],
            "City": "SampleCity",
            "StateProvinceCode": "CA",
            "PostalCode": "12345",
            "CountryCode": "US"
        }
        payment_info = {
           "ShipmentCharge": {
           "Type": "01",
           "BillShipper": {
            "AccountNumber": "RC6604",
            "Address": {
                "PostalCode": "93063",
                "CountryCode": "US"
            }
           }
}
}
        if not access_token:
            raise HTTPException(status_code=500, detail="Failed to retrieve UPS access token.")
        
        package_data = booking_data.get("package_details",[])
       
        # Validate ship_from_address
        ship_from_address ={
            "Name": booking_data.get("ship_from_address",{}).get("from_name"),
            "AddressLine": [booking_data.get("ship_from_address",{}).get("from_address")],
            "City":  booking_data.get("ship_from_address",{}).get("from_city"),
            "StateProvinceCode":  booking_data.get("ship_from_address",{}).get("from_state"),
            "PostalCode":  booking_data.get("ship_from_address",{}).get("from_pincode"),
            "CountryCode":  booking_data.get("ship_from_address",{}).get("from_country")

        }
        logger.info(f"ship_from_address: {ship_from_address}")

        # Validate ship_to_address
        ship_to_address ={
            "Name": booking_data.get("ship_to_address",{}).get("to_name"),
            "Phone": {"Number": booking_data.get("ship_to_address", {}).get("to_mobile", "")},
            "AddressLine": [booking_data.get("ship_to_address",{}).get("to_address")],
            "City":  booking_data.get("ship_to_address",{}).get("to_city"),
            "StateProvinceCode":  booking_data.get("ship_to_address",{}).get("to_state"),
            "PostalCode":  booking_data.get("ship_to_address",{}).get("to_pincode"),
            "CountryCode":  booking_data.get("ship_to_address",{}).get("to_country")

        }
        logger.info(f"ship_to_address from service: {ship_to_address}")
        
        booking_items = booking_data.get("booking_items",[])

        service_code = package_data.get("service_code",{})
        print(f"service_code from service: {service_code}")
       
        pickup_date = booking_data.get("pickup_date", "")
        logger.info(f"pickup_date from service: {pickup_date}")
        formatted_pickupdate = (
            datetime.strptime(pickup_date, "%Y%m%d").strftime("%Y-%m-%d")
            if isinstance(pickup_date, str) and pickup_date.isdigit() 
            else pickup_date
        )
        logger.info(f"Formatted Pickup Date: {formatted_pickupdate}")

        pickup_time = booking_data.get("pickup_time", "")
        logger.info(f"pickup_time from service: {pickup_time}")

        for item in booking_items:
          package_type = item.get("package_type")

          if not package_type:
            return {"error": "Missing 'package_type' in booking_items"}

        # Assign package attributes based on package_type_code
        if package_type == "Document":  # Document package type
            item["packagebilltype"] = "02"
            item["DocumentsOnlyIndicator"] = "Document"
            item["PackagingType"] = {"Code": "01"}  # UPS Letter
        else:  # Non-Document package type
            item["packagebilltype"] = "03"
            item["DocumentsOnlyIndicator"] = "Non-Document"
            item["PackagingType"] = {"Code": "02"}  # Other Packaging

        # Construct package details
        package_details = {
            "Packaging": {
                "Code": item.get("PackagingType", {}).get("Code", ""),
                "Description": "Nails"
            },
            "DeliveryTimeInformation": {
                "PackageBillType": item.get("packagebilltype", ""),
                "Pickup": {"Date": formatted_pickupdate, "Time": pickup_time}
            },
            "NumOfPieces": package_data.get("package_count"),
            "DocumentsOnlyIndicator": item.get("DocumentsOnlyIndicator", ""),
        }
        logger.info(f"package details from service in create booking shipment service: {package_details}")
     

        # Add dimensions only if it's a Non-Document package
        if item["DocumentsOnlyIndicator"] == "Non-Document":
            package_details["Dimensions"] = {
                "UnitOfMeasurement": {"Code": "IN", "Description": "Inches"},
                "Length": str(item.get("length", "")),
                "Width": str(item.get("width", "")),
                "Height": str(item.get("height", ""))
            }
            package_details["PackageWeight"] = {
                "UnitOfMeasurement": {"Code": "LBS", "Description": "Pounds"},
                "Weight": str(item.get("weight", ""))
            }
        print(f"package details from service: {package_details}")
        print(f"package details:{type(item.get("weight"))}")

        logger.info(f"Final package_details before UPS request: {json.dumps(package_details, indent=2)}")
        
        # Call UPS API to create shipment
        shipment_response = ups_create_shipment(
    access_token,
    shipper_address,
    ship_from_address,
    ship_to_address,
    package_details,
    service_code,  
    payment_info,  
    pickup_date,
    pickup_time,
)
         # Extract Tracking Number
        tracking_number = shipment_response.get("tracking_number", "N/A")
        booking_status = "Booked" if tracking_number != "N/A" else "Pending"
        base_service_charge = shipment_response.get("base_service_charge", "0.00")
        label_filename = shipment_response.get("label_filename", "")
        shipment_id = shipment_response.get("shipment_id", "N/A")
        total_charges = shipment_response.get("total_charges", "0.00")
        
        # **UPDATE BOOKING STATUS AND TRACKING NUMBER**
        new_booking.tracking_number = tracking_number
        new_booking.booking_status = booking_status
        db.commit()
        db.refresh(new_booking)

        logger.info(f"Booking {new_booking.booking_id} updated with Tracking Number: {tracking_number} and Status: {booking_status}")
        logger.info(f"shipment_response from service: {shipment_response}")
        logger.info(f"Booking Data at service layer: {booking_data}")
        logger.info(f"Extracted Pickup Date: {pickup_date}")
        logger.info(f"Extracted Pickup Time: {pickup_time}")

        if not shipment_response or "tracking_number" not in shipment_response:
            logger.error(f"UPS API error: {shipment_response}")
            raise HTTPException(status_code=500, detail="Invalid UPS API response.")

        return {
            "booking_status": new_booking.booking_status,
            "tracking_number": new_booking.tracking_number,
            "base_service_charge": base_service_charge,
            "label_filename": label_filename,
            "shipment_id": shipment_id,
            "total_charges": total_charges
        }

    except Exception as e:
        logger.error(f"Error in booking and shipment service: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating booking and shipment: {str(e)}")

  
# Business logics for cancel booking service (Mysql DB)
def cancel_booking_service(db: Session, booking_id: int):
    """Business logic to cancel a booking by setting active_flag=0 and updating booking_status to 'Cancelled'."""
    try:
        # Fetch the booking record
        booking = db.query(Bookings).filter(Bookings.booking_id == booking_id).first()

        if not booking:
            raise ValueError("Booking not found.")

        # Update fields
        booking.active_flag = 0
        booking.booking_status = "Cancelled"

        # Commit changes using CRUD
        return cancel_booking_status(db, booking)
    except Exception as e:
        raise Exception(f"Error canceling booking: {e}")   
  
       
# Business logics for get all bookings (Mysql DB)
def get_all_bookings_service(db: Session, booking_id: Optional[int] = None):
    """Fetch all bookings from the database."""
    try:
        bookings = get_all_bookings_crud(db, booking_id)
        return bookings  

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Service error while fetching bookings: {e}")
    

# Business logics for get all addressbook (Mysql DB)
def get_all_addressbook_service(db: Session):
    """Fetch all addressbooks from the database."""
    try:
        address_book = get_all_addresses(db)

        return address_book  

    except Exception as e:
        raise Exception(f"Service error while fetching all addressbook: {e}")


