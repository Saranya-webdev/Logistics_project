from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.databases.mysqldb import get_db
import logging
from app.schemas.carriers import CarrierCreate, CarrierResponse, CarrierUpdateResponse, CarrierUpdate, SuspendOrActiveRequest, SuspendOrActiveResponse
from app.service.carriers import create_carrier_service, update_carrier_service, suspend_or_activate_carrier, get_carrier_profile_service, get_carriers_profile_list_service


logger = logging.getLogger(__name__)

# Create a FastAPI router
router = APIRouter()

@router.post("/createcarrier/", response_model=CarrierResponse)
async def create_new_carrier(
    carrier_data: CarrierCreate,  
    db: Session = Depends(get_db)  
):  
    """
    Endpoint to create a new carrier. It validates the required fields and creates the carrier in the system.
    """
    try:
        result = create_carrier_service(db, carrier_data.dict())
        if "Error" in result["message"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating carrier: {str(e)}"
        )
    
# NEW FOR FORNTEND
@router.put("/updatecarrier", response_model=CarrierUpdateResponse, status_code=status.HTTP_200_OK)
async def update_carrier(carrier_data: CarrierUpdate, db: Session = Depends(get_db)):
    """
    Route for updating a carrier's details using the request body.
    """
    try:
        if not carrier_data.carrier_email: 
            raise HTTPException(status_code=400, detail="Carrier email is required for update.")

        carrier_data_dict = carrier_data.dict()
        updated_carrier = update_carrier_service(db, carrier_data.carrier_email, carrier_data_dict)

        if "message" in updated_carrier:  
            raise HTTPException(status_code=400, detail=updated_carrier["message"])

        return updated_carrier  

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.put("/updatecarrier", response_model=CarrierUpdateResponse, status_code=status.HTTP_200_OK, operation_id="update_carrier_unique")
async def update_carrier(carrier_data: CarrierUpdate, db: Session = Depends(get_db)):
    """
    Route for updating a carrier's details using the request body.
    """
    try:
        if not carrier_data.carrier_email:  
            raise HTTPException(status_code=400, detail="Carrier email is required for update.")

        carrier_data_dict = carrier_data.dict()

        updated_carrier = update_carrier_service(db, carrier_data.carrier_email, carrier_data_dict)  

        return updated_carrier  

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/suspend-or-activate/", response_model=SuspendOrActiveResponse)
async def update_carrier_status(
    update_request: SuspendOrActiveRequest,
    db: Session = Depends(get_db)
):
    """
    API to activate or suspend a carrier.
    """
    try:
        result = suspend_or_activate_carrier(db, **update_request.dict())
        return SuspendOrActiveResponse(**result)

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating carrier status: {str(e)}"
        )



@router.get("/{carrier_email}/profile", response_model=dict)
def get_carrier(carrier_email: str, db: Session = Depends(get_db)):
    """
    Retrieve the profile of a carrier based on their email.
    """
    try:
        profile =get_carrier_profile_service(db, carrier_email)
        return profile
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An unexpected error occurred: {str(e)}")

@router.get("/carriersprofilelist/", response_model=list)
def get_carriers_list(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all carrier profiles.
    """
    try:
        return get_carriers_profile_list_service(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
