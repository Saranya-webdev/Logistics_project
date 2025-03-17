from app.crud.quotations import update_quotation_crud,create_quotation_crud,get_all_quotations_crud,get_single_quotation_crud
from app.crud.bookings import save_quotation,update_quotation
import logging
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.utils.ups_utils import ups_get_access_token,get_ups_shipping_rates
import os


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


        print(f"Sending to UPS API: pickup_date={pickup_date}, pickup_time={pickup_time}")

        print(f"package details from service: {(package_data)}")  # Debugging print
        print(f"PackagingType from service: {package_data.get('PackagingType')}")
        print(f"PackageBillType from service: {package_data.get('packagebilltype')}")
        print(f"DocumentsOnlyIndicator from service: {package_data.get('DocumentsOnlyIndicator')}")

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
        # Prepare the quotation data directly
        quotation_data = {
            "quotation_id": ObjectId(),
            "address":{
            "ship_to": ship_to_address,
            "ship_from": ship_from_address,
            },
            
            "package_details": package_details,
            "status": "Unsaved",
            # "created_by": {
            #     "usertype": data.get("UserType", "") if data.get("UserType") else None,
            #     "userid": data.get("UserId","") if data.get("UserId") else None,
            # }
        }
        print(f"package details from service: {package_details}")

        # Save the initial quotation to DB
        quotation_result = await save_quotation(quotation_data)
        print(f"quotation id from service {(quotation_result.get("quotation_id"))}")
        quotation_id = quotation_result.get("quotation_id")

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

            update_result = await update_quotation(quotation_id, processed_shipping_rates)

        if not update_result.get("success"):
            return {"error": "Failed to update quotation with shipping rates."}

        return {"quotation_id": quotation_id, "shipping_rates": processed_shipping_rates}

    except Exception as e:
        return {"error": str(e)}

async def create_quotation_service(db, quotation_data: dict):
    try:
        quotation_data["_id"] = ObjectId() 
        quotation_data["quotation_id"] = str(quotation_data["_id"])  # Store as string

        structured_data = {
            "_id": quotation_data["_id"],
            "quotation_id": quotation_data["quotation_id"],
            "address": {
                "ship_to": quotation_data.get("ship_to_address", {}),
                "ship_from": quotation_data.get("ship_from_address", {})
            },
            "package_details": {
                "Packaging": {
                    "Code": "01",
                    "Description": "Nails"
                },
                "DeliveryTimeInformation": {
                    "PackageBillType": "02"
                },
                "Pickup": {
                    "Date": quotation_data.get("pickup_date", ""),
                    "Time": quotation_data.get("pickup_time", ""),
                    "NumOfPieces": quotation_data.get("package_count", 1),
                    "DocumentsOnlyIndicator": quotation_data["package_details"][0].get("package_type", "Document"),
                },
                "Dimensions": {
                    "UnitOfMeasurement": {
                        "Code": "IN",
                        "Description": "Inches"
                    },
                    "Length": quotation_data["package_details"][0].get("length", ""),
                    "Width": quotation_data["package_details"][0].get("width", ""),
                    "Height": quotation_data["package_details"][0].get("height", ""),
                },
                "PackageWeight": {
                    "UnitOfMeasurement": {
                        "Code": "LBS",
                        "Description": "Pounds"
                    },
                    "Weight": int(quotation_data["package_details"][0].get("weight", 0)),
                }
            },
            "status": "Unsaved",
            "shipping_rates": quotation_data.get("shipping_rates", [])
        }

        result = await create_quotation_crud(db, structured_data)

        if result.inserted_id:
            return structured_data 
        else:
            raise Exception("Failed to create quotation")

    except Exception as e:
        raise Exception(f"Error in creating quotation: {str(e)}")

    
async def update_quotation_service(db, quotation_id: str, quotation_data: dict):
    try:
        # Ensure quotation_data is a dictionary
        if not isinstance(quotation_data, dict):
            raise ValueError("Quotation data should be a dictionary, not a string.")

        # Convert the QuotationStatus enum to a string if it's present
        if "status" in quotation_data:
            quotation_data["status"] = quotation_data["status"].value  # Convert enum to string

        # Check if quotation_id needs to be converted to ObjectId
        if len(quotation_id) == 24:  # Length of ObjectId is always 24
            quotation_id = ObjectId(quotation_id)

        # Filter based on quotation_id
        filter_criteria = {"quotation_id": quotation_id}

        # Prepare the updated quotation data
        updated_quotation = {
            "pickup_date": quotation_data.get("pickup_date", ""),
            "pickup_time": quotation_data.get("pickup_time", ""),
            "package_count": quotation_data.get("package_count", 1),
            "package_details": quotation_data.get("package_details", []),
            "status": quotation_data.get("status", "Saved"), 
        }

        # Call the CRUD operation to update the quotation
        result = await update_quotation_crud(db, filter_criteria, updated_quotation)

        if result.matched_count == 0:
            return {"message": "No matching quotation found for update.", "modified_count": 0}

        return {"message": "Quotation updated successfully", "modified_count": result.modified_count}

    except Exception as e:
        raise Exception(f"Error in updating quotation: {str(e)}")
    

async def get_single_quotation_service(quotation_id: str, db: AsyncIOMotorDatabase):
    try:
        quotation = await get_single_quotation_crud(quotation_id, db)
        if not quotation:
            return None  # Return None if quotation is not found

        address_data = quotation.get("address", {})

        # Extract and format package details
        package_details_raw = quotation.get("package_details", [])

        # Ensure package_details is a list
        if not isinstance(package_details_raw, list):
            package_details_raw = [package_details_raw]

        # Process each package entry
        package_details = []
        for package in package_details_raw:
            dimensions = package.get("Dimensions", {})
            package_weight = package.get("PackageWeight", {})

            # Determine package_type: Use `package_type` if available, else use `DocumentsOnlyIndicator`
            package_type = package.get("package_type", "").strip()
            if not package_type:  
                package_type = package.get("DocumentsOnlyIndicator", "").strip()

            package_details.append({
                "weight": str(package_weight.get("Weight", "0")),
                "length": dimensions.get("Length", ""),
                "width": dimensions.get("Width", ""),
                "height": dimensions.get("Height", ""),
                "package_type": package_type 
            })

        processed_quotation = {
            "_id": str(quotation["_id"]),
            "quotation_id": str(quotation.get("quotation_id")),
            "address": {
                "ship_to": address_data.get("ship_to", {}),
                "ship_from": address_data.get("ship_from", {}),
            },
            "package_details": package_details,
            "status": quotation.get("status"),
            "shipping_rates": quotation.get("shipping_rates", []),
            "from_pincode": quotation.get("from_pincode"),
            "package_count": quotation.get("package_count"),
            "pickup_date": quotation.get("pickup_date"),
            "pickup_time": quotation.get("pickup_time"),
            "to_pincode": quotation.get("to_pincode"),
        }

        return processed_quotation

    except Exception as e:
        raise Exception(f"Error retrieving quotation: {str(e)}")

async def get_all_quotations_service(db: AsyncIOMotorDatabase):
    try:
        quotations = await get_all_quotations_crud(db)
        print("Raw Quotation Data:", quotations[:1])

        processed_quotations = []
        for quotation in quotations:
            address_data = quotation.get("address", {})

            # Extract and format package details correctly
            package_details_raw = quotation.get("package_details", [])

            # Ensure package_details is a list
            if not isinstance(package_details_raw, list):
                package_details_raw = [package_details_raw]

            # Process each package entry
            package_details = []
            for package in package_details_raw:
                dimensions = package.get("Dimensions", {})
                package_weight = package.get("PackageWeight", {})

                # Determine package_type: Use `package_type` if available, else use `DocumentsOnlyIndicator`
                package_type = package.get("package_type", "").strip()
                if not package_type:
                    package_type = package.get("DocumentsOnlyIndicator", "").strip()

                package_details.append({
                    "weight": str(package_weight.get("Weight", "0")),  # Ensure weight is a string
                    "length": dimensions.get("Length", ""),
                    "width": dimensions.get("Width", ""),
                    "height": dimensions.get("Height", ""),
                    "package_type": package_type 
                })

                print("Processed Package Details:", package_details[-1])

            processed_quotation = {
                "_id": str(quotation["_id"]),
                "quotation_id": str(quotation.get("quotation_id")),
                "address": {
                    "ship_to": address_data.get("ship_to", {}),
                    "ship_from": address_data.get("ship_from", {}),
                },
                "package_details": package_details,
                "status": quotation.get("status"),
                "shipping_rates": quotation.get("shipping_rates", []),
                "from_pincode": quotation.get("from_pincode"),
                "package_count": quotation.get("package_count"),
                "pickup_date": quotation.get("pickup_date"),
                "pickup_time": quotation.get("pickup_time"),
                "to_pincode": quotation.get("to_pincode"),
            }

            processed_quotations.append(processed_quotation)

        return processed_quotations

    except Exception as e:
        raise Exception(f"Error processing quotations: {str(e)}")

