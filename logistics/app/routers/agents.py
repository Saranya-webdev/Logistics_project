from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.agents import AgentCreate,  AgentResponse, AgentUpdate, AgentUpdateResponse,AgentBookingListResponse
from app.models.agents import Agent
from app.databases.mysqldb import get_db
import logging
from app.crud.agents import update_agent, get_agents_and_bookings, soft_delete_agent ,fetch_all_agents_with_bookings,create_agent,get_agent
from app.service.agents import update_agent_service, verify_agent_service, suspend_or_activate_agent,get_agent_profile, get_agent_booking_list

router = APIRouter() 

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Define the POST endpoint for creating an agent
@router.post("/agents", status_code=status.HTTP_201_CREATED)
def create_agent(agent_data: AgentCreate, db: Session = Depends(get_db)):
    """
    API endpoint to create a new agent.
    """
    try:
        # Call the service to create an agent
        result = create_agent(db, agent_data.dict())

        if result.get("message") == "Agent already exists":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Agent with this mobile number already exists."
            )

        # Return the result if successful
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
    

@router.post("/suspend-or-activate-agent/")
def suspend_or_activate_agent_route(agent_mobile: str, active_flag: int, remarks: str, db: Session = Depends(get_db)):
    """
    Suspend or activate a agent based on their mobile and active_flag.
    The status of the agent is updated along with any remarks provided.
    """
    updated_agent = suspend_or_activate_agent(db, agent_mobile, active_flag, remarks)
    return {"message": "Agent status updated", "agent": updated_agent}    

@router.post("/verifyagent/")
async def verify_agent(agent_mobile: str, verification_status: str, db: Session = Depends(get_db)):
    """
    Verify the agent by email and mobile, and update the verification status and active flag.
    If the status is 'Verified', the active flag is set to 1.
    """
    # Step 1: Call the service to verify the agent
    result = verify_agent_service(db, agent_mobile, verification_status)

    # Step 2: If no agent is found, return an error
    if "message" in result and result["message"] == "No agents found":
        raise HTTPException(status_code=404, detail="No agents found")

    # Step 3: Return the updated agent response
    return result


@router.get("/{agent_mobile}/profile", response_model=dict)
def get_agent_profile_endpoint(agent_mobile: str, db: Session = Depends(get_db)):
    """
    Retrieve the profile of an agent based on their mobile number.
    """
    try:
        profile = get_agent_profile(db, agent_mobile)
        return profile
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An unexpected error occurred: {str(e)}")


@router.get("/agentslistbookinglist/", response_model=list)
def get_agents_with_bookings(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all agents with their booking summaries.
    """
    return fetch_all_agents_with_bookings(db)


# Get agent with booking list
@router.get("/{agent_id}/bookinglist/", response_model=AgentBookingListResponse)
def get_agent_booking_list_endpoint(agent_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the list of bookings associated with agent, identified by their agent ID.
    """
    return get_agent_booking_list(agent_id, db)
    
# Get agent booking details
@router.get("/{agent_id}/bookings/{booking_id}/", response_model=AgentBookingListResponse)
def get_booking_details(
    agent_id: int,
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve details for a specific booking of a agent identified by their agent ID and booking ID.
    """
    from app.crud.agents import get_agent_booking_details
    try:
        return get_agent_booking_details(db, agent_id, booking_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while fetching booking details.")    
    

# Update agent by ID
@router.put("/{agent_id}/updateagent", response_model=AgentUpdateResponse, status_code=status.HTTP_200_OK)
async def edit_agent(agent_id: int, agent: AgentUpdate, db: Session = Depends(get_db)):
    """
    Update the details of an existing agent identified by their agent ID.
    Fields are updated only if provided in the request body.
    """
    # Step 1: Check if any fields are provided for update
    if not any(value is not None for value in agent.dict(exclude_unset=True).values()):
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Step 2: Check if the agent exists
    existing_agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not existing_agent:
        raise HTTPException(status_code=404, detail="Agent ID not found")
    
    # Step 3: Call the update_agent function to update agent data
    updated_agent = update_agent(db, agent_id, agent.dict(exclude_unset=True))
    
    # Step 4: Return the updated agent response
    return updated_agent


# Delete agent by ID
@router.delete("/{agent_id}/deleteagent", status_code=status.HTTP_200_OK)
async def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """
    Soft delete a agent identified by their agent ID. 
    The agent is marked as deleted but the record is not removed from the database.
    """
    agent = get_agent(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    if agent.deleted:
        raise HTTPException(status_code=400, detail="Agent already marked as deleted")
    
    # Proceed with soft delete if agent exists and isn't deleted yet
    soft_delete_agent(db, agent_id)
    return {"detail": f"Agent {agent.agent_name} (ID: {agent.agent_id}) marked as deleted successfully"}


