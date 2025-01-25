from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.databases.mysqldb import get_db
import logging
from app.schemas.thisaiprofiles import AssociatesCreate, AssociatesResponse, AssociatesUpdateResponse, AssociatesUpdate, AssociatesCredentialCreate, AssociatesCredentialResponse
from app.crud.thisaiprofiles import create_associates_crud, update_associates_by_id, suspend_or_activate_associates_crud, get_associates_profile_crud, get_associates_profiles_list_crud, soft_delete_associates_crud, verify_associate_crud

logger = logging.getLogger(__name__)

# Create a FastAPI router
router = APIRouter()

@router.post("/createassociates/", response_model=AssociatesResponse, status_code=status.HTTP_201_CREATED)
async def create_associates(
    associates_data: AssociatesCreate,  # associates data will be passed in the request body
    db: Session = Depends(get_db)  # Database session dependency
):
    """
    Endpoint to create a new associates. It validates the required fields and creates the associates in the system.
    """
    try:
        # Log the received associates data
        logger.debug(f"Received associates data: {associates_data}")

        # Call the CRUD function to create the associates in the database
        result = create_associates_crud(db=db, associates_data=associates_data.dict())

        if isinstance(result, dict) and "message" in result:
            if result["message"] == "associates created successfully":
                return AssociatesResponse(**result)  # Return the associates creation success response
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result["message"]
                )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while creating associates."
        )

    except Exception as e:
        logger.error(f"Error in creating associates: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating associates: {str(e)}"
        )
    

# @router.post("/create-associate-credential/", response_model=AssociatesCredentialResponse, status_code=status.HTTP_201_CREATED)
# async def create_associate_credential(
#     associate_credential: AssociatesCredentialCreate,  # associate credential data will be passed in the request body
#     db: Session = Depends(get_db)  # Database session dependency
# ):
#     """
#     Endpoint to create an associate credential by matching the email. It validates the required fields and creates the associate credential.
#     """
#     try:
#         # Log the received associate credential data
#         logger.debug(f"Received associate credential data: {associate_credential}")

#         # Call the CRUD function to create the associate credential in the database
#         result = create_associate_credential(db=db, associate_credential=associate_credential)  # Adjusted call

#         # Check if the result contains a success message
#         if isinstance(result, dict) and "message" in result:
#             if result["message"] == "Associate credential created successfully.":
#                 return AssociatesCredentialResponse(**result)  # Return the associate credential creation success response
#             else:
#                 raise HTTPException(
#                     status_code=status.HTTP_400_BAD_REQUEST,
#                     detail=result["message"]
#                 )

#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Error occurred while creating associate credential."
#         )

#     except Exception as e:
#         logger.error(f"Error in creating associate credential: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error creating associate credential: {str(e)}"
#         )


@router.post("/suspend-or-activate/", status_code=status.HTTP_200_OK)
async def update_associates_status(
    associates_mobile: str,  # This must match the query parameter name
    active_flag: int,
    remarks: str,
    db: Session = Depends(get_db)
):
    """
    API to activate or suspend a associates.
    """
    try:
        # Validate input for active_flag to ensure it's 1 or 2
        if active_flag not in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="active_flag must be 1 (active) or 2 (suspend)"
            )
        
        result = suspend_or_activate_associates_crud(db, associates_mobile, active_flag, remarks)
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating associates status: {str(e)}"
        )

@router.post("/verifyassociate/{associates_mobile}")
def verify_associate(
    associates_mobile: str,
    verification_status: str,
    db: Session = Depends(get_db)
):
    """
    Endpoint to verify the associate and update their status and active flag.

    Args:
        associates_mobile (str): Mobile number of the associate.
        verification_status (str): Verification status ('Verified' or 'Not Verified').
        db (Session): Database session.

    Returns:
        dict: Updated associate details or error message.
    """
    try:
        # Call the CRUD function to verify the associate and update the status
        result = verify_associate_crud(db, associates_mobile, verification_status)
        return result
    
    except HTTPException as http_exc:
        # Propagate HTTPExceptions raised by the CRUD function
        raise http_exc
    
    except Exception as e:
        # Catch unexpected errors and raise a 500 Internal Server Error with the error message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while verifying the associate: {str(e)}"
        )

@router.get("/{associates_mobile}/profile", response_model=dict)
def get_associates_profile_endpoint(associates_mobile: str, db: Session = Depends(get_db)):
    """
    Retrieve the profile of a associates based on their mobile number.
    """
    try:
        # Call the CRUD method to get the associates profile
        profile = get_associates_profile_crud(db, associates_mobile)
        return profile
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An unexpected error occurred: {str(e)}")


@router.get("/associatessprofilelist/", response_model=list)
def get_associatess(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all associates profiles.
    """
    try:
        # Attempt to fetch all associates profiles from the service layer
        return get_associates_profiles_list_crud(db)
    except HTTPException as e:
        # If an HTTPException is raised, return it as is
        raise e
    except Exception as e:
        # For other types of exceptions, raise a general 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.put("/{associates_id}/updateassociates", response_model=AssociatesUpdateResponse, status_code=status.HTTP_200_OK)
def edit_associates(associates_id: int, associates: AssociatesUpdate, db: Session = Depends(get_db)):
    """
    Update the details of an existing associates identified by their associates ID.
    Fields are updated only if provided in the request body.
    """
    try:
        updated_associates = update_associates_by_id(db, associates_id, associates.dict())  # .dict() to convert Pydantic model to a dictionary
        return updated_associates
    except Exception as e:
        logger.error(f"Error updating associates: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating associates: {str(e)}")
    

@router.delete("/{associates_id}/soft-delete", response_model=dict)
def soft_delete_associates_endpoint(associates_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to soft delete a associates based on their ID.
    """
    try:
        # Call the service layer for soft deletion
        deleted_associates = soft_delete_associates_crud(db, associates_id)
        return {"message": "associates soft-deleted successfully", "associates_id": deleted_associates.associates_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while soft deleting the associates: {str(e)}"
        )