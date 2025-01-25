from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.databases.mysqldb import get_db
import logging
from app.schemas.agents import AgentCreate, AgentResponse, AgentUpdateResponse, AgentUpdate
from app.crud.agents import create_agent_crud, update_agent_by_id, suspend_or_activate_agent_crud, get_agent_profile_crud, get_agent_profiles_list_crud, soft_delete_agent_crud

logger = logging.getLogger(__name__)

# Create a FastAPI router
router = APIRouter()

@router.post("/createagent/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,  # agent data will be passed in the request body
    db: Session = Depends(get_db)  # Database session dependency
):
    """
    Endpoint to create a new agent. It validates the required fields and creates the agent in the system.
    """
    try:
        # Log the received agent data
        logger.debug(f"Received agent data: {agent_data}")

        # Call the CRUD function to create the agent in the database
        result = create_agent_crud(db=db, agent_data=agent_data.dict())

        if isinstance(result, dict) and "message" in result:
            if result["message"] == "agent created successfully":
                return AgentResponse(**result)  # Return the agent creation success response
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result["message"]
                )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while creating agent."
        )

    except Exception as e:
        logger.error(f"Error in creating agent: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating agent: {str(e)}"
        )
    
@router.put("/{agent_id}/updateagent", response_model=AgentUpdateResponse, status_code=status.HTTP_200_OK)
def edit_agent(agent_id: int, agent: AgentUpdate, db: Session = Depends(get_db)):
    """
    Update the details of an existing agent identified by their agent ID.
    Fields are updated only if provided in the request body.
    """
    try:
        updated_agent = update_agent_by_id(db, agent_id, agent.dict())  # .dict() to convert Pydantic model to a dictionary
        return updated_agent
    except Exception as e:
        logger.error(f"Error updating agent: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating agent: {str(e)}")


@router.post("/suspend-or-activate/", status_code=status.HTTP_200_OK)
async def update_agent_status(
    agent_mobile: str,  # This must match the query parameter name
    active_flag: int,
    remarks: str,
    db: Session = Depends(get_db)
):
    """
    API to activate or suspend a agent.
    """
    try:
        # Validate input for active_flag to ensure it's 1 or 2
        if active_flag not in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="active_flag must be 1 (active) or 2 (suspend)"
            )
        
        result = suspend_or_activate_agent_crud(db, agent_mobile, active_flag, remarks)
        return result
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating agent status: {str(e)}"
        )


@router.get("/{agent_mobile}/profile", response_model=dict)
def get_agent_profile_endpoint(agent_mobile: str, db: Session = Depends(get_db)):
    """
    Retrieve the profile of a agent based on their mobile number.
    """
    try:
        # Call the CRUD method to get the agent profile
        profile = get_agent_profile_crud(db, agent_mobile)
        return profile
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An unexpected error occurred: {str(e)}")

@router.get("/agentsprofilelist/", response_model=list)
def get_agents(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all agent profiles.
    """
    try:
        # Attempt to fetch all agent profiles from the service layer
        return get_agent_profiles_list_crud(db)
    except HTTPException as e:
        # If an HTTPException is raised, return it as is
        raise e
    except Exception as e:
        # For other types of exceptions, raise a general 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.delete("/{agent_id}/soft-delete", response_model=dict)
def soft_delete_agent_endpoint(agent_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to soft delete a agent based on their ID.
    """
    try:
        # Call the service layer for soft deletion
        deleted_agent = soft_delete_agent_crud(db, agent_id)
        return {"message": "agent soft-deleted successfully", "agent_id": deleted_agent.agent_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while soft deleting the agent: {str(e)}"
        )