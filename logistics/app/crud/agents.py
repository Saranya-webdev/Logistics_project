from app.models.agents import Agent  # Correct import
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging
from app.utils import log_and_raise_exception  # Correct import
from typing import Optional
from datetime import datetime


logger = logging.getLogger(__name__)

# Helper functions
def log_success(message: str):
    logging.info(message)

def log_error(message: str, status_code: int):
    logging.error(f"{message} - Status Code: {status_code}")

# CRUD operations for agent
def create_agent_crud(db: Session, agent_data: dict) -> dict:
    """CRUD operation for creating a agent."""
    from app.service.agents import create_agent_service

    logger.debug(f"Received agent data: {agent_data}")

    try:
        result = create_agent_service(db, agent_data)
        
        if isinstance(result, dict):
            return result
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating agent")
    except HTTPException as e:
        logger.error(f"Error in agent creation: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating agent: {str(e)}")


def update_agent_by_id(db: Session, agent_id: int, agent_data: dict) -> dict:
    """Update a agent's details based on agent ID."""
    from app.service.agents import update_agent_service

    try:
        # Call the update_agent_service to handle the business logic
        result = update_agent_service(db, agent_id, agent_data)

        # If the result from the service layer contains a message (such as 'No agents found'), raise HTTPException
        if "message" in result:
            if result["message"] == "No agents found":
                raise HTTPException(status_code=404, detail="agent not found")  # Status code 404 for not found
            else:
                raise HTTPException(status_code=400, detail=result["message"])  # Status code 400 for client errors

        # Return the successful result from the service layer
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating agent: {str(e)}")  # Status code 500 for server errors


def update_agent_status(db: Session, agent: Agent, active_flag: int, remarks: Optional[str] = None) -> None:
    """Update agent's active status and remarks."""
    try:
        agent.active_flag = active_flag
        if remarks is not None:
            agent.remarks = remarks
        db.commit()
        db.refresh(agent)  # Ensure the agent object is updated with new values
    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error updating agent status: {str(e)}", 500)



def get_agent_by_mobile(db: Session, agent_mobile: str) -> Agent:
    """Retrieve a agent from the database based on their mobile number."""
    try:
        agent = db.query(agent).filter(agent.agent_mobile == agent_mobile).first()
        if not agent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="agent not found")
        return agent
    except Exception as e:
        log_and_raise_exception(f"Error retrieving agent by mobile {agent_mobile}: {str(e)}", 500)

def get_agent_profile_crud(db: Session, agent_mobile: str) -> dict:
    """Call the service to retrieve a agent's profile based on mobile number."""
    from app.service.agents import get_agent_profile
    try:
        # Call the service function to get the agent profile
        profile = get_agent_profile(db, agent_mobile)
        return profile
    except HTTPException as e:
        # Raise the exception if the agent is not found
        raise e
    except Exception as e:
        # Log and raise a generic exception for other errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving agent profile: {str(e)}"
        )

def get_agent_profiles_list_crud(db: Session) -> list:
    """Retrieve a list of all agent profiles from the service layer."""
    from app.service.agents import get_agents_profile_list
    try:
        # Call the service function to get the list of all agent profiles
        agent_profiles = get_agents_profile_list(db)
        return agent_profiles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching agent profiles: {str(e)}"
        )


def suspend_or_activate_agent_crud(db: Session, agent_mobile: str, active_flag: int, remarks: str):
    """Suspend or activate agent."""
    from app.service.agents import suspend_or_activate_agent
    
    try:
        updated_agent = suspend_or_activate_agent(db, agent_mobile, active_flag, remarks)
        return updated_agent
    except Exception as e:
        log_and_raise_exception(f"Error in suspend or activate agent: {str(e)}", 500)


def soft_delete_agent_crud(db: Session, agent_id: int):
    """Soft delete the agent by setting the 'deleted' flag to True."""
    agent = db.query(agent).filter(agent.agent_id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="agent not found")
    
    # Set the deleted flag and mark the deletion time
    agent.deleted = True
    agent.deleted_at = datetime.utcnow()
    db.add(agent)
    db.commit()
    
    return agent