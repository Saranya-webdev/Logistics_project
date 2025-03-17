from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException, status
from app.models.agents import Agent, Category, AgentCredential
from app.models.bookings import Bookings
from app.schemas.agents import AgentUpdateResponse
from app.utils.utils import log_and_raise_exception, populate_dynamic_entries
import logging
from typing import Optional



# Configure logger
logger = logging.getLogger(__name__)

# Helper functions
def log_success(message: str):
    logging.info(message)

def log_error(message: str, status_code: int):
    logging.error(f"{message} - Status Code: {status_code}")

# CRUD operations for create Agent
def create_agent_crud(db: Session, agent_data: dict) -> Agent:
    """Create a new agent in the database."""
    try:
       # Create an Agent object using the data passed in
       new_agent = Agent(**agent_data)
    
       # Add the agent to the session and commit to the database
       db.add(new_agent)
       db.commit()
       db.refresh(new_agent)
       return new_agent
    except Exception as e:
        db.rollback()
        raise Exception(f"Database error in create_agent_crud: {e}")


def create_agent_credential(db: Session, agent_id: int, email_id: str, password: str):
    """Inserts a new agent credential into the database."""
    try:
        agent_credential = AgentCredential(
            agent_id=agent_id,  
            email_id=email_id,  #  Ensure this matches the agentCredential table
            password=password  
        )

        db.add(agent_credential)
        db.commit()
        db.refresh(agent_credential)
        return agent_credential
    except Exception as e:
        db.rollback()
        raise Exception(f"Database error in create_agent_credential: {e}")
    

def update_agent_password_crud(db: Session, credential: AgentCredential, hashed_password: str):
    """Updates an associate's password in the database."""
    try:
        credential.password = hashed_password  # Update the password field

        db.commit()  # Commit transaction
        db.refresh(credential)  # Refresh instance from DB

        return credential
    except Exception as e:
        db.rollback()  # Rollback in case of failure
        raise Exception(f"Database error while updating password in update_agent_password_crud: {e}")    

    
# CRUD operations for get Agent profile
def get_agent_profile_crud(db: Session, agent_email: str):
    """
    Retrieve an agent from the database based on their email.
    """
    try:
        # Query the agent based on their email
        agent = db.query(Agent).filter(Agent.agent_email == agent_email).first()
        return agent
    except Exception as e:
        raise Exception(f"Database error while retrieving agent in get_agent_profile_crud: {str(e)}")


# CRUD operations for get all Agents
def get_all_agents_crud(db: Session) -> list:
    """
    Retrieve all agents from the database.
    """
    try:
        agents = db.query(Agent).all()
        return agents
    except Exception as e:
        raise Exception(f"Database error while retrieving all agents in get_all_agents_crud: {str(e)}")
    

def get_bookings_by_agent_crud(db: Session, agent_email: str, booking_id: Optional[int] = None):
    """
    Fetch bookings from the database where booking is placed by an agent.
    """
    try:
        query = db.query(Bookings).filter(Bookings.booking_by == agent_email)

        if booking_id:
            query = query.filter(Bookings.booking_id == booking_id)

        query =  query.options(
           joinedload(Bookings.booking_items)
       )
        bookings = query.all()  # Ensure `all()` is called on a valid query object

        if not bookings:
            logging.warning(f"No bookings found for agent_email {agent_email} with booking_id {booking_id}")

        return bookings

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving agent booking list in get_bookings_by_agent_crud: {str(e)}"
        )



# CRUD operations for update agent
def update_agent_crud(db: Session, agent: Agent, agent_data: dict) -> Agent:
    """Update an agent with new data based on agent email (excluding email modification)."""
    try:
        for key, value in agent_data.items():
            if hasattr(agent, key):
                setattr(agent, key, value)

        db.commit()
        db.refresh(agent)  # Ensure updated values are fetched
        return agent
    except Exception as e:
        db.rollback()  # Rollback in case of failure
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating agent in update_agent_crud: {str(e)}"
        )




# CRUD operations for verify Agent
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
        raise Exception(f"Database error while updating agent verification in verify_agent_crud: {str(e)}")
    

# CRUD operations for suspend/active Agent
def suspend_or_active_agent_crud(db: Session, agent_email: str, active_flag: int, remarks: str):
    """Suspend or activate agent in the database."""
    try:
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
    except Exception as e:
        log_error(f"Error in suspend or active agent in CRUD: {str(e)}", 500)
        raise


# Additional functions for populating categories and types
def populate_categories(db: Session):
    """Populate agent categories."""
    categories = [Category.tier_1, Category.tier_2, Category.tier_3]
    try:
        populate_dynamic_entries(db, Agent, categories, 'agent_category')
        log_success("Agent categories populated successfully")
    except Exception as e:
        log_error(f"Error populating categories in populate_categories CRUD: {str(e)}", 500)
        raise