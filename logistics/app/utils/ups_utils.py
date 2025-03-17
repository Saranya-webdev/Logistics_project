import requests
import base64
import json
from datetime import datetime
from PIL import Image
import io
import os



import requests

async def get_ups_shipping_rates(access_token, shipper_address, ship_to_address, ship_from_address, package_details,pickup_date,pickup_time, package_count):
  """
  Retrieves shipping rates and transit times from the UPS API.

  Args:
      shipper_address (dict): Dictionary containing shipper address information.
      ship_to_address (dict): Dictionary containing ship-to address information.
      ship_from_address (dict): Dictionary containing ship-from address information.
      package_details (dict): Dictionary containing package details.
      service_code (str): UPS service code (e.g., "03" for Ground).
      payment_info (dict): Dictionary containing payment information.
      version (str, optional): API version. Defaults to "v2409".
      requestoption (str, optional): Request option (e.g., "Shoptimeintransit"). Defaults to "Shoptimeintransit".

  Returns:
      dict: JSON response from the UPS API, or None if the request fails.
  """

  # url = f"https://wwwcie.ups.com/api/rating/{version}/{requestoption}"
  version = "v2409"
  requestoption = "Shoptimeintransit"
  url = "https://wwwcie.ups.com/api/rating/" + version + "/" + requestoption

  payload = {
    "RateRequest": {
      "Request": {
        "TransactionReference": {
          "CustomerContext": "CustomerContext"
        }
      },
      "Shipment": {
        "Shipper": {
          "Name": shipper_address.get("Name", ""),
          "ShipperNumber": "RC6604",
          "Address": {
            "AddressLine": shipper_address.get("AddressLine", []),
            "City": shipper_address.get("City", ""),
            "StateProvinceCode": shipper_address.get("StateProvinceCode", ""),
            "PostalCode": shipper_address.get("PostalCode", ""),
            "CountryCode": shipper_address.get("CountryCode", "")
          }
        },
        "ShipTo": {
          "Name": ship_to_address.get("Name", ""),
          "Address": {
            "AddressLine": ship_to_address.get("address_line_1", []),
            "City": ship_to_address.get("city", ""),
            "StateProvinceCode": ship_to_address.get("stateprovince", ""),
            "PostalCode": ship_to_address.get("postal_code", ""),
            "CountryCode": ship_to_address.get("country_code", "")
          }
        },
        "ShipFrom": {
          "Name": ship_from_address.get("Name", ""),
          "Address": {
            "AddressLine": ship_from_address.get("address_line_1", []),
            "City": ship_from_address.get("city", ""),
            "StateProvinceCode": ship_from_address.get("stateprovince", ""),
            "PostalCode": ship_from_address.get("postal_code", ""),
            "CountryCode": ship_from_address.get("country_code", "")
          }
        },
        "PaymentDetails": {
        "ShipmentCharge": [
          {
            "Type": "01",
            "BillShipper": {
              "AccountNumber": "RC6604"
            }
          }
        ]
      },
    "PickupType": {"Code": "06"},
        "DeliveryTimeInformation": {
          "PackageBillType": package_details["DeliveryTimeInformation"]["PackageBillType"],  
          #"Pickup": {"Date": package_details["DeliveryTimeInformation"]["Pickup"]["Date"]}
                          #"PackageBillType": package_data.get("packagebilltype", ""),
          # "Pickup": {"Date": pickup_date}
          "Pickup": {
            "Date": pickup_date, 
            "Time": pickup_time
          }
        },
        "NumOfPieces": package_count,
        "Package": {
          "PackagingType": {
            "Code": package_details["Packaging"]["Code"],
            "Description": package_details["Packaging"]["Description"]
           }
          
        }
      }
    }
  }
  payload["RateRequest"]["Shipment"]["Package"]["PackageWeight"] = package_details.get("PackageWeight", {
    "UnitOfMeasurement": {"Code": "LBS", "Description": "Pounds"},
    "Weight": "1"
})
  # Ensure weight is a string
  payload["RateRequest"]["Shipment"]["Package"]["PackageWeight"]["Weight"] = str(payload["RateRequest"]["Shipment"]["Package"]["PackageWeight"]["Weight"])
  # Conditionally add Dimensions and PackageWeight if it's a Non-Document package
  if package_details["DocumentsOnlyIndicator"] == "Non-Document":
    payload["RateRequest"]["Shipment"]["Package"]["Dimensions"] = package_details["Dimensions"]

# Conditionally add DocumentsOnlyIndicator
  if package_details.get("DocumentsOnlyIndicator"):
    payload["RateRequest"]["Shipment"]["DocumentsOnlyIndicator"] = package_details["DocumentsOnlyIndicator"]

    print(f"pickup date inside ups_utils: {package_details}")
    print(f"package details inside ups_utils: {package_details}")
    print(f"packagebilltype inside ups_utils: {package_details.get('PackageBillType')}")
    print(f"packagebilltype from deliverytimeinformation: {package_details['DeliveryTimeInformation']['PackageBillType']}")
    print(f"documentonlyindicator inside ups_utils: {package_details.get('DocumentsOnlyIndicator')}")
    print(f"ship from address in ups_utils: {ship_from_address}")
    print(f"ship to address in ups_utils: {ship_to_address}")



  headers = {
    "Content-Type": "application/json",
    "transId": "12345",  # Replace with your unique transaction ID
    "transactionSrc": "testing",
    "Authorization": f"Bearer {access_token}",
  }

  try:
    response = requests.post(url, json=payload, headers=headers)    
    responsedata=json.loads(response.text)
    print("UPS SHIPPING RATES :::::::::::",responsedata)
    if responsedata:
      # Process the response data
            try:
                rate_list = []
                for shipment in responsedata['RateResponse'].get('RatedShipment', []):  # Use .get to handle potential missing key
                  
                    service_code = shipment['Service']['Code']
                    service_desc = shipment['Service']['Description']
                    service_name= shipment['TimeInTransit']['ServiceSummary']['Service']['Description']
                    transit_time = shipment['TimeInTransit']['ServiceSummary']['EstimatedArrival']['BusinessDaysInTransit']
                    # doc=shipment['TimeInTransit']['DocumentsOnlyIndicator']
                    estimated_arrival_date=shipment['TimeInTransit']['ServiceSummary']['EstimatedArrival']['Arrival']['Date']
                    estimated_arrival_time=shipment['TimeInTransit']['ServiceSummary']['EstimatedArrival']['Arrival']['Time']
                    total_charges = shipment['TotalCharges']['MonetaryValue']
                    dayofweek=shipment['TimeInTransit']['ServiceSummary']['EstimatedArrival']['DayOfWeek']

                    # Format date and time
                    formatted_date = datetime.strptime(estimated_arrival_date, "%Y%m%d").strftime("%B %d, %Y")
                    formatted_time = datetime.strptime(estimated_arrival_time, "%H%M%S").strftime("%I:%M %p")

                    rate_details = {
                    "service_code": shipment['Service']['Code'],
                    "service_desc" : shipment['Service']['Description'],
                    "service_name": shipment['TimeInTransit']['ServiceSummary']['Service']['Description'],
                    "transit_time": shipment['TimeInTransit']['ServiceSummary']['EstimatedArrival']['BusinessDaysInTransit'],
                    "estimated_arrival_date": formatted_date,
                    "estimated_arrival_time": formatted_time,
                    "dayofweek":dayofweek,
                    "total_charges": shipment['TotalCharges']['MonetaryValue'],
                    # "doc":doc
                    }
                    rate_list.append(rate_details)

                    print(f"Service: {service_code} - {service_desc}")
                    print(f"Service Desc: {service_desc}")
                    print(f"Service name : {service_name}")
                    print(f"Transit Time: {transit_time} business days")
                    print(f"Estimated Arrival Date & Time : {estimated_arrival_date}  - {estimated_arrival_time}")
                    print(f"Total Charges: ${total_charges}")
                    print("-" * 20) 
            except KeyError as e:
                print(f"Error parsing response data: {e}")
            else:
                print("Failed to retrieve shipping rates.")     
    return rate_list
  except requests.exceptions.RequestException as e:
    print(f"Error making UPS API request: {e}")
    return None
  
def ups_get_access_token(client_id, client_secret):
    """
    Fetches an access token from the UPS API using client credentials.

    Args:
        client_id: Your UPS Developer Portal client ID.
        client_secret: Your UPS Developer Portal client secret.

    Returns:
        The access token as a string, or None if the request fails.
    """

    auth_string = f"{client_id}:{client_secret}"
    base64_encoded_auth = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

    headers = {
        "Authorization": f"Basic {base64_encoded_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post("https://onlinetools.ups.com/security/v1/oauth/token", headers=headers, data=data)
   
    data = json.loads(response.text)
  
    if response.status_code == 200:
        return data["access_token"]
        
    else:
        print(f"Error fetching access token: {response.text}")
        return None
    
def ups_address_validation(access_token, address_json):

    requestoption = "3"
    version = "v2"
    url = "https://wwwcie.ups.com/api/addressvalidation/" + version + "/" + requestoption

    try:
        #address_data = json.loads(address_json)
        address_data = address_json 
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format for address data")

    # Extract address information from address_data
    address_lines = address_data.get("AddressLine", [])
    city = address_data.get("City")
    state = address_data.get("StateProvinceCode")
    postal_code = address_data.get("PostalCode")
    country_code = address_data.get("CountryCode")
    consignee_name = address_data.get("Name")  # Include ConsigneeName (or similar)

    # Validate required fields
    if not all([consignee_name, city, state, postal_code, country_code]):
        raise ValueError("Missing required fields in address data")

    # Build the payload with dynamic address information
    payload = {
        "XAVRequest": {
            "AddressKeyFormat": {
                "ConsigneeName": consignee_name, 
                "AddressLine": address_lines,
                "City": city,
                "PoliticalDivision1": state, 
                "PostcodePrimaryLow": postal_code,
                "CountryCode": country_code
            }
        }
    }

    
    query = {
    "regionalrequestindicator": "string",
    "maximumcandidatelistsize": "1"
    }
    """
    payload = {
    "XAVRequest": {
        "AddressKeyFormat": {
        "ConsigneeName": "Ramalingam",
        "BuildingName": "Innoplex",
        "AddressLine": [
            "1834 Blazewood Street, Simi Valley",
            "STE D",
            "ALISO VIEJO TOWN CENTER"
        ],
        "Region": "Simi Valley",
        "PoliticalDivision2": "",
        "PoliticalDivision1": "CA",
        "PostcodePrimaryLow": "93063",
        "PostcodeExtendedLow": "1521",
        "Urbanization": "Simi Valley",
        "CountryCode": "US"
        }
    }
    }
"""
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",
    #"Authorization": "Bearer eyJraWQiOiI2NGM0YjYyMC0yZmFhLTQzNTYtYjA0MS1mM2EwZjM2Y2MxZmEiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzM4NCJ9.eyJzdWIiOiJtYWlsbWF0aGlAZ21haWwuY29tIiwiY2xpZW50aWQiOiI3V1NueEtuY0NNYTVtaEJaSVB3TXY1enhuaFhSc05USXQ1ejZJd3NpY2llTnJkRzIiLCJpc3MiOiJodHRwczovL2FwaXMudXBzLmNvbSIsInV1aWQiOiI2QjhGOTc0NC05OUYzLTEwMTQtOTdFMC1BQjg1MTYzQjU3MEIiLCJzaWQiOiI2NGM0YjYyMC0yZmFhLTQzNTYtYjA0MS1mM2EwZjM2Y2MxZmEiLCJhdWQiOiJtYWR1cmFpMzYwIiwiYXQiOiJuQkR6VVhtdEtQSG42RnhjN1hHSjlYSFI4VUFYIiwibmJmIjoxNzM0MTEzODEwLCJzY29wZSI6IkxvY2F0b3JXaWRnZXQiLCJEaXNwbGF5TmFtZSI6Im1hZHVyYWkzNjAiLCJleHAiOjE3MzQxMjgyMTAsImlhdCI6MTczNDExMzgxMCwianRpIjoiNGQxMTVlYjItOTUwMi00YzgxLWIwYjctMGViNTQ4OTRhYzhiIn0.gdK6E4F4k6Q70ZikoC_B4LbEaJTZOgpWOL-HX5SAqiTpz_Tc_HYrVJx2lKx1E1BUVacgKPju4glbN7GQ7v36iZ0EhvPopbEn2eL2aejuk2E9WgJ7MJ91k7nPxkzw6OVPATCMVnJ020Rrb8oCU9CIJUISQ4g8KFO8SKLrXRrY6hJz0LTOC7i_V58RlEvtAtq9Bg_bMu0vpoz5hUeZVbY2qLoVnqK0IIACmv3TBo005-icxFphup7nXx2RNBu1ijVgq14cwdyHL6Mz-IR0bLN_N3UEC7EuAJy2amS5oUEYe3nNxBk3b7bWlDJTgS40yfnWPFHOnqnmxQI2mtV7CqSBf-F28DnwWXtMkg-WmXMxGyTT1Vn_f7KMDiCDYvyOW413Tt-INiRLK2Gonux5dcH3QPw5ZT100MfGn4kEzwCo6fm_NfkNjooShvHahpXEt4Rv1hY5wbmUktkvvl9ki40zipcKl-if1ksi56yOQ2HECseht9rvW4e3kaKc66nv6OLV_AwicyVIWPCjFLXVFwWjC_EgA_9I-EAdk9Q_kbe91BHzPvUZA3khd3WfkSLRlvjtwMFfcVJKQe-zI4TE4ywjwpdd1YLYU-AfBPYOhpv7-n06Sa9kmGbfUuKcYSGQOh1vd6Sg8DtqK8l3hwubDHVTZhm9WVgtGkR58Wl9IQEbRdU"
    }

    response = requests.post(url, json=payload, headers=headers, params=query)

    data = response.json()
    #print(data)
    print("\n\n")


def ups_create_shipment(access_token, shipper_address, ship_from_address, ship_to_address, 
                           package_details, service_code, payment_info, pickup_date, pickup_time):
    print(f"package_details from ups utils", package_details)

    version = "v2409"
    # url = "https://wwwcie.ups.com/api/shipments/" + version + "/ship"
    url = "https://onlinetools.ups.com/api/shipments/" + version + "/ship"

    query = {
    "additionaladdressvalidation": "string"
    }
    print(f"payment info from ups_utils: {payment_info}")

    payload = {
        "ShipmentRequest": {
            "Request": {
                "SubVersion": "1801",
                "RequestOption": "nonvalidate",
                "TransactionReference": {
                    "CustomerContext": ""
                }
            },
            "Shipment": {
                "Description": "Ship WS test",
                "Shipper": {
                    "Name": shipper_address.get("Name"),
                     "ShipperNumber": "RC6604",
                    "Address": shipper_address
                },
                "ShipFrom": {
                    "Name": ship_from_address.get("Name"),
                    "Address": ship_from_address
                },
                "ShipTo": {
                    "Name": ship_to_address.get("Name"),
                    "Address": ship_to_address
                },
                "Package": package_details,
                "Service": {
                    "Code": service_code
                },
                "PaymentInformation": payment_info
            },
            "Pickup": {
                "Date": pickup_date,
                "Time": pickup_time
            },
        
                 "LabelSpecification": {
                    "LabelImageFormat": {
                        "Code": "PNG"
                    }
                }
        }
    }

    headers = {
    "Content-Type": "application/json",
    "transId": "12345",
    "transactionSrc": "testing",
    "Authorization": f"Bearer {access_token}",
    #"Authorization": "Bearer eyJraWQiOiI2NGM0YjYyMC0yZmFhLTQzNTYtYjA0MS1mM2EwZjM2Y2MxZmEiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzM4NCJ9.eyJzdWIiOiJtYWlsbWF0aGlAZ21haWwuY29tIiwiY2xpZW50aWQiOiI3V1NueEtuY0NNYTVtaEJaSVB3TXY1enhuaFhSc05USXQ1ejZJd3NpY2llTnJkRzIiLCJpc3MiOiJodHRwczovL2FwaXMudXBzLmNvbSIsInV1aWQiOiI2QjhGOTc0NC05OUYzLTEwMTQtOTdFMC1BQjg1MTYzQjU3MEIiLCJzaWQiOiI2NGM0YjYyMC0yZmFhLTQzNTYtYjA0MS1mM2EwZjM2Y2MxZmEiLCJhdWQiOiJtYWR1cmFpMzYwIiwiYXQiOiJlSUE3S2VYaVhnM21BZGdOTVB0Z0x5V0d1QlFWIiwibmJmIjoxNzM0NDU4NTY0LCJzY29wZSI6IkxvY2F0b3JXaWRnZXQiLCJEaXNwbGF5TmFtZSI6Im1hZHVyYWkzNjAiLCJleHAiOjE3MzQ0NzI5NjQsImlhdCI6MTczNDQ1ODU2NCwianRpIjoiZDMyODJhMGItYmZkNC00OWExLWE1OGQtMDcxZDU2OTExNWY4In0.FcO_eYloaEYwSWVEcPntu60OaJ76riEeK3EitvAj0od_9Tn1NKehsZmcuXZ0CbxTWlN1YJqWm8Opgrlck2OWSK2B0kbYjlAUvSuwdP7tpdReZIT7nJFfpJ8QnwWzi8nmCCurM2qQQkUR669K9J1saP32TN8zDEUldSrm5utZ61g0ke4tKQ2xbRHogAGEpLKN4Mi7gDyrpYjpZ72CoocECredPQSyNt8byGCRvjvNcR2D1k5jeSB03E4DGJX23F8cDVLsy4nFKTTb19YKy8IRijQwf2ZKvQTjEJ1rp9XP9AA1KGkICuoKeaU1eMLByWKyBeR-K4hb8J_c0iy3M9SeAgwSb4VZtGKFuHq5u-aaZzhpSJFiGvXvg-ju0Rsxdfd161WpCtSrCwvuW3n0fWWxsCbMzvtr39dytpGMSMxoimdJA_9IBJtdeFx7WPy9GvHaUaYNqMSn1ImKMQc_RZT1gDrMkn6-bdjRe-TuPLtcNHhDQMVro4iVcIdj252ienj9MmhxVQMwQS5J7tRPt8h8ly3kMuHDCEVeafIJBHBIXwvRrnZjo1lpK9xwag9EakDdKweYMrQKlhPkNJnZNmHToDM_e5P29lxrgXapyX5WbgGj6190fPFwxBIfQ2Wuo76-qyThPophc0npLrmRxxRVqZyyUoM8eFfmfSCWGRoSWVE"
    }

    response = requests.post(url, json=payload, headers=headers, params=query)

    data = response.json()
    print("Create Shipping Response  :::::::",data)

    shipment_response = data.get("ShipmentResponse", {})
    shipment_results = shipment_response.get("ShipmentResults", {})
    package_results = shipment_results.get("PackageResults",[])
    if not package_results:
            raise ValueError("package details not available")
    

    # Accessing Shipment Identification Number
    shipment_id = shipment_results.get('ShipmentIdentificationNumber') 
        # Accessing Tracking Number
    tracking_number = package_results[0].get('TrackingNumber') 
        # Accessing Total Charges
    total_charges = shipment_results.get('ShipmentCharges',{}).get('TotalCharges',{}).get('MonetaryValue')
        # Accessing Base Service Charge
    base_service_charge = package_results[0].get('BaseServiceCharge',{}).get('MonetaryValue') 

        # Accessing a specific Rate Modifier (e.g., Demand Surcharge - Residential)
    residential_surcharge = None
        # Accessing Shipping Label Image (Base64 encoded)
    shipping_label_image = shipment_results.get("ShippingLabel", {}).get("GraphicImage") or shipment_results.get("PackageResults", [{}])[0].get("ShippingLabel", {}).get("GraphicImage")


    if shipping_label_image:
            # Save shipping label
            label_filename = save_shipping_label(shipping_label_image, shipment_id)
    else:
            label_filename = None

    shipment_details = {
            "shipment_id": shipment_id,
            "tracking_number": tracking_number,
            "total_charges": total_charges,
            "base_service_charge": base_service_charge,
            "residential_surcharge": residential_surcharge,
            "label_filename": label_filename,
        }

    print("\nshipment_id : ", shipment_id)
    print("\nTracking Number : ", tracking_number)
    print("\nTotal Charge : ", total_charges)
    print("\nBase Service Charge : ", base_service_charge)
    print("\nResidential Surcharge : ", residential_surcharge)
    return shipment_details


def save_shipping_label(shipping_label_image, shipment_id):
    """Saves the shipping label image with the shipment ID as the filename.

    Args:
        data: The JSON response data from the UPS API.
        shipment_id: The shipment identification number retrieved from the response.
    """
    try:
        # Check for valid Base64-encoded image data
        if not isinstance(shipping_label_image, str):
            raise ValueError("Shipping label image is not a string.")

        # Decode Base64 image
        img_bytes = base64.b64decode(shipping_label_image)

        # Define the new save location
        save_dir = r"C:\Users\saran\thisai\courier_frontend\public\shipment_labels"

        # Ensure the directory exists
        os.makedirs(save_dir, exist_ok=True)

        # Try opening the image using both GIF and PNG formats
        try:
            img = Image.open(io.BytesIO(img_bytes))
            filename = f"{shipment_id}.gif"
            file_path = os.path.join(save_dir, filename)
            img.save(file_path)
            print(f"Shipping label saved as: {file_path}")
            return f"shipment_labels/{filename}"
        except (IOError, SyntaxError):
            # If opening as GIF fails, attempt PNG
            try:
                img = Image.open(io.BytesIO(img_bytes))
                filename = f"{shipment_id}.png"
                file_path = os.path.join(save_dir, filename)
                img.save(file_path)
                print(f"Shipping label saved as: {file_path} (as PNG)")
                return f"shipment_labels/{filename}"
            except (IOError, SyntaxError) as e:
                print(f"Error saving image: {e}")
                return None

    except ValueError as e:
        print(f"ValueError: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
