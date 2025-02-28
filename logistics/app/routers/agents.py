from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
<<<<<<< HEAD
from app.schemas.agents import AgentCreate, AgentResponse, AgentUpdate, AgentUpdateResponse, SuspendOrActiveResponse, SuspendOrActiveRequest, VerifyStatusResponse, VerifyStatusRequest, AgentCredentialCreate, AgentCredentialResponse, AgentPasswordUpdate,AgentBookingListResponse
from app.databases.mysqldb import get_db
import logging
from app.service.agents import update_agent_service, verify_agent_service, suspend_or_activate_agent, get_agent_profile, get_all_agents_profile, create_agent_service, create_agent_credential_service, update_agent_password_service, get_bookings_by_agent_service
=======
from app.schemas.agents import AgentCreate, AgentResponse, AgentUpdate, AgentUpdateResponse, SuspendOrActiveResponse, SuspendOrActiveRequest, VerifyStatusResponse, VerifyStatusRequest, AgentCredentialCreate, AgentCredentialResponse, AgentPasswordUpdate
from app.databases.mysqldb import get_db
import logging
from app.service.agents import update_agent_service, verify_agent_service, suspend_or_activate_agent, get_agent_profile, get_all_agents_profile, create_agent_service, create_agent_credential_service, update_agent_password_service
>>>>>>> origin/main

router = APIRouter()

# Configure logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Define the POST endpoint for creating an agent
@router.post("/createagent", response_model=AgentResponse)
async def create_new_agent(agent_data: AgentCreate, db: Session = Depends(get_db)):
    """
    API endpoint to create a new agent.
    """
    try:
        logger.debug(f"Received agent_data: {agent_data}")
        result = create_agent_service(db, agent_data.dict())  # Explicitly call the CRUD function

        if result.get("message") == "Agent already exists":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Agent with this mobile number already exists."
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
    

@router.post("/agent-credentials/", response_model=AgentCredentialResponse)
def create_agent_credential(
    agent_data: AgentCredentialCreate,  
    db: Session = Depends(get_db)
):
    """API to create agent credentials"""
    try:
    
       agent_credential = create_agent_credential_service(
       db, 
       agent_data.agent_id, 
       agent_data.agent_email, 
       agent_data.password
       )

       if not agent_credential:
          raise HTTPException(status_code=400, detail="agent ID and Email do not match.")

       return AgentCredentialResponse(
        agent_credential_id=agent_credential.agent_credential_id,
        agent_id=agent_credential.agent_id,
        email_id=agent_credential.email_id,  
        password=agent_credential.password  #  Consider removing from response for security
        )
    except Exception as e:
        logger.error(f"Error while creating agent's credentails: {str(e)}")
        db.rollback()
        raise


@router.put("/agent/update-password", response_model=dict)
def update_agent_password(data: AgentPasswordUpdate, db: Session = Depends(get_db)):
    """API endpoint to update an associate's password."""
    try:
        updated_credential = update_agent_password_service(db, data.agent_id, data.new_password)
        
        return {
            "message": "Password updated successfully",
            "agent_id": updated_credential.agent_id
        }
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@router.post("/suspend-or-activate/", response_model=SuspendOrActiveResponse)
async def update_agent_status(
    update_request: SuspendOrActiveRequest,
    db: Session = Depends(get_db)
):
    """
    API to activate or suspend an agent.
    """
    try:
        # Call the function to update agent status
        result = suspend_or_activate_agent(
            db, 
            **update_request.dict()
        )
        
        # FastAPI will automatically serialize the returned dict
        return result["agent"]  # Returning only the 'agent' portion for the response model

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating agent status: {str(e)}"
        )



@router.post("/verify-agent", response_model=VerifyStatusResponse)
async def update_agent_status(
    update_status: VerifyStatusRequest,
    db: Session = Depends(get_db)
):
    try:
        updated_agent = verify_agent_service(
            db, 
            update_status.agent_email,
            update_status.verification_status
        )
        return updated_agent  

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get("/{agent_email}/profile", response_model=dict)
def get_agent_profile_endpoint(agent_email: str, db: Session = Depends(get_db)):
    """
    Retrieve the profile of an agent based on their email.
    """
    try:
        profile = get_agent_profile(db, agent_email)
        return profile
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An unexpected error occurred: {str(e)}")


@router.get("/agentsprofilelist/", response_model=list)
def get_all_agents_profiles_endpoint(db: Session = Depends(get_db)):
    """
    Retrieve the profiles of all agents.
    """
    try:
        profiles = get_all_agents_profile(db)
        return profiles
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An unexpected error occurred: {str(e)}")


<<<<<<< HEAD
@router.get("/{agent_email}/bookings", response_model=AgentBookingListResponse)
def get_bookings_by_agent(agent_email: str, db: Session = Depends(get_db)):
    """
    Retrieve the list of bookings placed by an agent.
    """
    try:
        return get_bookings_by_agent_service(db, agent_email)
    except HTTPException as http_ex:
        raise http_ex  # Re-raise FastAPI HTTP exceptions
    except Exception as e:
        logging.error(f"Error retrieving bookings for agent {agent_email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error. Please try again later.")

=======
>>>>>>> origin/main

# Update agent by ID
@router.put("/updateagent", response_model=AgentUpdateResponse, status_code=status.HTTP_200_OK)
async def update_agent(agent_data: AgentUpdate, db: Session = Depends(get_db)):
    """
    Route for updating an agent's details using the request body.
    """
    if not agent_data.agent_email:
        raise HTTPException(status_code=400, detail="Agent email is required for update.")

    agent_data_dict = agent_data.dict()

    updated_agent = update_agent_service(db, agent_data_dict)

    if "message" in updated_agent:
        raise HTTPException(status_code=400, detail=updated_agent["message"])

    return updated_agent

