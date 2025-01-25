from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.databases.mysqldb import get_db
import logging
from app.schemas.carriers import CarrierCreate, CarrierResponse, CarrierUpdateResponse, CarrierUpdate
from app.crud.carriers import create_carrier_crud, update_carrier_by_id, suspend_or_activate_carrier_crud, get_carrier_profile_crud, get_carrier_profiles_list_crud, soft_delete_carrier_crud

logger = logging.getLogger(__name__)

# Create a FastAPI router
router = APIRouter()

@router.post("/createcarrier/", response_model=CarrierResponse, status_code=status.HTTP_201_CREATED)
async def create_carrier(
    carrier_data: CarrierCreate,  # Carrier data will be passed in the request body
    db: Session = Depends(get_db)  # Database session dependency
):
    """
    Endpoint to create a new carrier. It validates the required fields and creates the carrier in the system.
    """
    try:
        # Log the received carrier data
        logger.debug(f"Received carrier data: {carrier_data}")

        # Call the CRUD function to create the carrier in the database
        result = create_carrier_crud(db=db, carrier_data=carrier_data.dict())

        if isinstance(result, dict) and "message" in result:
            if result["message"] == "Carrier created successfully":
                return CarrierResponse(**result)  # Return the carrier creation success response
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result["message"]
                )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while creating carrier."
        )

    except Exception as e:
        logger.error(f"Error in creating carrier: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating carrier: {str(e)}"
        )
    
@router.put("/{carrier_id}/updatecarrier", response_model=CarrierUpdateResponse, status_code=status.HTTP_200_OK)
def edit_carrier(carrier_id: int, carrier: CarrierUpdate, db: Session = Depends(get_db)):
    """
    Update the details of an existing carrier identified by their carrier ID.
    Fields are updated only if provided in the request body.
    """
    try:
        updated_carrier = update_carrier_by_id(db, carrier_id, carrier.dict())  # .dict() to convert Pydantic model to a dictionary
        return updated_carrier
    except Exception as e:
        logger.error(f"Error updating carrier: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating carrier: {str(e)}")


@router.post("/suspend-or-activate/", status_code=status.HTTP_200_OK)
async def update_carrier_status(
    carrier_mobile: str,  # This must match the query parameter name
    active_flag: int,
    remarks: str,
    db: Session = Depends(get_db)
):
    """
    API to activate or suspend a carrier.
    """
    try:
        # Validate input for active_flag to ensure it's 1 or 2
        if active_flag not in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="active_flag must be 1 (active) or 2 (suspend)"
            )
        
        result = suspend_or_activate_carrier_crud(db, carrier_mobile, active_flag, remarks)
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating carrier status: {str(e)}"
        )


@router.get("/{carrier_mobile}/profile", response_model=dict)
def get_carrier_profile_endpoint(carrier_mobile: str, db: Session = Depends(get_db)):
    """
    Retrieve the profile of a carrier based on their mobile number.
    """
    try:
        # Call the CRUD method to get the carrier profile
        profile = get_carrier_profile_crud(db, carrier_mobile)
        return profile
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An unexpected error occurred: {str(e)}")

@router.get("/carriersprofilelist/", response_model=list)
def get_carriers(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all carrier profiles.
    """
    try:
        # Attempt to fetch all carrier profiles from the service layer
        return get_carrier_profiles_list_crud(db)
    except HTTPException as e:
        # If an HTTPException is raised, return it as is
        raise e
    except Exception as e:
        # For other types of exceptions, raise a general 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.delete("/{carrier_id}/soft-delete", response_model=dict)
def soft_delete_carrier_endpoint(carrier_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to soft delete a carrier based on their ID.
    """
    try:
        # Call the service layer for soft deletion
        deleted_carrier = soft_delete_carrier_crud(db, carrier_id)
        return {"message": "Carrier soft-deleted successfully", "carrier_id": deleted_carrier.carrier_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while soft deleting the carrier: {str(e)}"
        )