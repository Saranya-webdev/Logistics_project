from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.agents import Agent, Category
from app.schemas.agents import AgentUpdateResponse
from app.utils import log_and_raise_exception, populate_dynamic_entries
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
def create_agent_crud(db: Session, agent_data: dict) -> Agent:
    """Create a new agent in the database."""
    # Create an Agent object using the data passed in
    new_agent = Agent(**agent_data)
    
    # Add the agent to the session and commit to the database
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)
    
    return new_agent

def get_agent_profile_crud(db: Session, agent_email: str):
    """
    Retrieve an agent from the database based on their email.
    """
    try:
        # Query the agent based on their email
        agent = db.query(Agent).filter(Agent.agent_email == agent_email).first()
        return agent
    except Exception as e:
        raise Exception(f"Database error while retrieving agent: {str(e)}")


def get_all_agents_crud(db: Session) -> list:
    """
    Retrieve all agents from the database.
    """
    try:
        agents = db.query(Agent).all()
        return agents
    except Exception as e:
        raise Exception(f"Database error while retrieving all agents: {str(e)}")


def update_agent_crud(db: Session, agent: Agent, agent_data: dict) -> Agent:
    """Update an agent with new data based on agent email (excluding email modification)."""
    # Update the agent's fields using agent_data
    for key, value in agent_data.items():
        if hasattr(agent, key) and value is not None:
            setattr(agent, key, value)

    db.commit()
    db.refresh(agent)

    # Return the updated agent response
    return agent


def verify_agent_crud(db: Session, agent_email: str, verification_status: str, active_flag: int):
    """
    Update the verification status and active flag for the agent in the database.
    """
    try:
        # Retrieve the agent based on the email
        existing_agent = db.query(Agent).filter(Agent.agent_email == agent_email).first()

        if not existing_agent:
            return None  # No agent found with the provided email

        # Update the agent's verification status and active flag
        existing_agent.verification_status = verification_status
        existing_agent.active_flag = active_flag

        # Commit the changes to the database
        db.commit()
        db.refresh(existing_agent)

        return existing_agent
    except Exception as e:
        db.rollback()  # Roll back changes if there's an error
        raise Exception(f"Database error while updating agent verification: {str(e)}")
    

def suspend_or_active_agent_crud(db: Session, agent_email: str, active_flag: int, remarks: str):
    """Suspend or activate agent in the database."""
    agent = db.query(Agent).filter(Agent.agent_email == agent_email).first()

    if not agent:
        return None

    # Update the agent's status and remarks
    agent.active_flag = active_flag
    agent.remarks = remarks

    # Commit the changes to the database
    db.commit()
    db.refresh(agent)

    return agent

def soft_delete_agent_crud(db: Session, agent_email: str):

    """Soft delete the agent."""
    try:
        agent = db.query(Agent).filter(Agent.agent_email == agent_email).first()

        # If the agent does not exist, return None
        if not agent:
            return None

        # Mark the agent as deleted
        agent.deleted = True
        agent.deleted_at = datetime.utcnow()

        # Save changes to the database
        db.add(agent)
        db.commit()
        db.refresh(agent)

        return agent
    except Exception as e:
        # Handle any database errors
        raise Exception(f"Error soft deleting agent: {str(e)}")


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