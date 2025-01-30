from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.databases.mysqldb import get_db
import logging
from app.schemas.thisaiprofiles import AssociatesCreate, AssociatesResponse, AssociatesUpdateResponse, AssociatesUpdate,SuspendOrActiveRequest,SuspendOrActiveResponse, VerifyStatusRequest, VerifyStatusResponse, DeleteRequest, DeleteResponse
from app.service.thisaiprofiles import create_associates_service, update_associates_service, suspend_or_activate_associates_service,verify_associate_service, soft_delete_associate_service, get_associates_profile_service, get_associatess_profile_list

logger = logging.getLogger(__name__)

# Create a FastAPI router
router = APIRouter()

@router.post("/createassociates/", response_model=AssociatesResponse)
async def create_new_associates(
    associates_data: AssociatesCreate,  # associates data will be passed in the request body
    db: Session = Depends(get_db)  # Database session dependency
):
    """
    Endpoint to create a new associate. It validates the required fields and creates the associate in the system.
    """
    try:
        # Log the received associates data
        logger.debug(f"Received associates data: {associates_data}")

        # Call the service layer to create the associate
        result = create_associates_service(db, associates_data.dict())

        if result.get("message") == "Associate already exists":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Associate with this email already exists."
            )
        return result
    
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred. Please try again later."
        )



@router.post("/suspend-or-activate/", response_model=SuspendOrActiveResponse)
async def update_associates_status(
    update_request: SuspendOrActiveRequest,
    db: Session = Depends(get_db)
):
    """
    API to activate or suspend an associate.
    """
    try:
        # Unpack the dictionary into keyword arguments
        result = suspend_or_activate_associates_service(
            db, 
            **update_request.dict()
        )
        return result

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating associate status: {str(e)}"
        )
    

@router.post("/verifyassociate", response_model=VerifyStatusResponse)
async def update_associates_status(
    update_status: VerifyStatusRequest,
    db: Session = Depends(get_db)
):
    try:
        updated_associate = verify_associate_service(
            db, 
            update_status.associates_email,
            update_status.verification_status
        )
        return updated_associate  

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )




@router.get("/{associates_email}/profile", response_model=dict)
def get_associates_profile_endpoint(associates_email: str, db: Session = Depends(get_db)):
    """
    Retrieve the profile of an associate based on their email.
    """
    try:
        return get_associates_profile_service(db, associates_email)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.get("/associates/profile-list", response_model=list)
def get_associates_profiles(db: Session = Depends(get_db)):
    """
    API Endpoint to retrieve all associates profiles.
    """
    try:
        return get_associatess_profile_list(db)  # Call service layer
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.put("/updateassociate", response_model=AssociatesUpdateResponse, status_code=status.HTTP_200_OK)
async def update_associate(associate_data: AssociatesUpdate, db: Session = Depends(get_db)):
    """
    Route for updating an associate's details using the request body.
    """
    if not associate_data.associates_email:  # Ensure proper field name is used
        raise HTTPException(status_code=400, detail="Associate email is required for update.")

    associate_data_dict = associate_data.dict()

    updated_associate = update_associates_service(db, associate_data.associates_email, associate_data_dict)  # Passing email separately

    if "message" in updated_associate:
        raise HTTPException(status_code=400, detail=updated_associate["message"])

    return updated_associate
    

@router.delete("/soft-delete", response_model=DeleteResponse)
def soft_delete_associate_endpoint(delete_request: DeleteRequest, db: Session = Depends(get_db)):
    """
    Endpoint to soft delete an associate based on their email.
    """
    try:
        # Extract email from the request body
        associates_email = delete_request.associates_email
        
        # Call the service layer for soft deletion
        deleted_associate = soft_delete_associate_service(db, associates_email)
        
        # Ensure the response model fields match exactly
        return DeleteResponse(
            associates_id=deleted_associate.associates_id,
            associates_name=deleted_associate.associates_name,  # Ensure this is included
            associates_email=deleted_associate.associates_email
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while soft deleting the associate: {str(e)}"
        )
