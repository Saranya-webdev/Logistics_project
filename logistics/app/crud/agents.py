from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.agents import Agent, Category
from app.models.bookings import Bookings
from app.schemas.agents import AgentUpdateResponse
from app.utils import log_and_raise_exception, populate_dynamic_entries, check_existing_agent_by_mobile
import logging
from datetime import datetime
from typing import Optional

# Configure logger
logger = logging.getLogger(__name__)

# Helper functions
def log_success(message: str):
    logging.info(message)

def log_error(message: str, status_code: int):
    logging.error(f"{message} - Status Code: {status_code}")


# CRUD operations for Agent
def create_agent(db: Session, agent_data: dict) -> dict:
    """CRUD operation for creating an agent, calling business logic from create_agent_service."""
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



def get_agent_by_mobile(db: Session, agent_mobile: str) -> Agent:
    """Retrieve an agent from the database based on their mobile number."""
    try:
        agent = check_existing_agent_by_mobile(db, agent_mobile)
        if not agent:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
        return agent
    except Exception as e:
        log_and_raise_exception(f"Error retrieving agent by mobile {agent_mobile}: {str(e)}", 500)


def get_agent_by_id(db: Session, agent_id: int) -> Agent:
    """Retrieve a agent by their ID."""
    return db.query(Agent).filter(Agent.agent_id == agent_id).first()


def get_agent(db: Session, agent_id: int):
    return db.query(Agent).filter(Agent.agent_id == agent_id).first()

def fetch_all_agents_with_bookings(db: Session) -> list:
    """
    Wrapper function to call the service function that retrieves all agents with their booking list summaries.
    """
    from app.service.agents import get_all_agents_with_booking_list
    return get_all_agents_with_booking_list(db)


def get_agents_and_bookings(db: Session, agent_id: int):
    """Retrieve agent and their bookings based on agent_id."""
    try:
        agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        bookings = db.query(Bookings).filter(Bookings.agent_id == agent_id).all()

        return agent, bookings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching agent with bookings: {str(e)}")




def get_agent_booking_details(db: Session, agent_id: int, booking_id: int):
    """CRUD layer function that calls the service layer to get booking details."""
    from app.service.agents import get_agent_with_booking_details

    return get_agent_with_booking_details(db, agent_id, booking_id)


def update_agent(db: Session, agent_data: dict) -> dict:
    """Update an agent with new data based on agent email."""
    # Query for agent by email instead of agent_id
    agent = db.query(Agent).filter(Agent.agent_email == agent_data["agent_email"]).first()

    if agent:
        # Exclude fields that shouldn't be updated (verification_status, category, notes)
        fields_to_exclude = ["verification_status", "agent_category", "notes"]
        filtered_data = {key: value for key, value in agent_data.items() if key not in fields_to_exclude}

        # Update agent details with the filtered data
        for key, value in filtered_data.items():
            setattr(agent, key, value)

        db.commit()
        db.refresh(agent)

        # Return the updated agent response
        return {
            "agent_id": agent.agent_id,
            "agent_name": agent.agent_name,
            "agent_email": agent.agent_email,
            "agent_mobile": agent.agent_mobile,
            "agent_address": agent.agent_address,
            "agent_city": agent.agent_city,
            "agent_state": agent.agent_state,
            "agent_country": agent.agent_country,
            "agent_pincode": agent.agent_pincode,
            "agent_geolocation": agent.agent_geolocation,
            "agent_businessname": agent.agent_businessname,
            "tax_id": agent.tax_id,
            "active_flag": agent.active_flag if agent.active_flag is not None else 0,
        }

    raise HTTPException(status_code=404, detail="No agents found")



def update_agent_status(db: Session, agent: Agent, active_flag: int, remarks: Optional[str] = None) -> None:
    """Update agent's active status and remarks."""
    try:
        agent.active = active_flag
        if remarks is not None:
            agent.remarks = remarks
        db.commit()
    except Exception as e:
        db.rollback()
        log_and_raise_exception(f"Error updating agent status: {str(e)}", 500)


def update_agent_verification_status(db: Session, agent_email: str, agent_mobile: str, verification_status: str) -> None:
    """Update agent's verification status and active flag in the database."""
    try:
        # Query for agent based on email and mobile
        agent = db.query(Agent).filter(Agent.agent_email == agent_email, Agent.agent_mobile == agent_mobile).first()

        if not agent:
            raise Exception("Agent not found")  # Raise error if agent doesn't exist

        # Update the verification status and active flag based on verification status
        if verification_status.lower() == "verified":
            agent.verification_status = verification_status
            agent.active_flag = 1  # Set active flag to 1 if verified
        else:
            agent.verification_status = verification_status  # Update status only if not verified

        db.commit()  # Commit changes to the database

    except Exception as e:
        db.rollback()
        raise Exception(f"Error updating agent verification status: {str(e)}")



def soft_delete_agent(db: Session, agent_id: int):
    """Soft delete the agent."""
    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent.deleted = True
    agent.deleted_at = datetime.utcnow()
    db.add(agent)
    db.commit()
    return agent


def suspend_or_active_agent_crud(db: Session, agent_mobile: str, active_flag: int, remarks: str):
    """Suspend or activate agent."""
    from app.service.agents import suspend_or_activate_agent
    
    updated_agent = suspend_or_activate_agent(db, agent_mobile, active_flag, remarks)
    return updated_agent


# Additional functions for populating categories and types
def populate_categories(db: Session):
    """Populate agent categories."""
    categories = [Category.tier_1, Category.tier_2, Category.tier_3]
    try:
        populate_dynamic_entries(db, Agent, categories, 'agent_category')
        log_success("Agent categories populated successfully")
    except Exception as e:
        log_error(f"Error populating categories: {str(e)}", 500)
        raise
