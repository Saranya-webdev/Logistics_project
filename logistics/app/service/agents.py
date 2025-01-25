from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.agents import Agent
from app.utils import check_existing_by_email
import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

def create_agent_service(db: Session, agent_data: dict) -> dict:
    """
    Business logic for creating an agent.
    """
    try:
        # Log validation process
        logger.info("Validating if the agent already exists...")

        # Check if agent already exists using email
        if check_existing_by_email(db, Agent, "agent_email", agent_data["agent_email"]):
            return {"message": "agent already exists"}

        # Ensure all required fields are present (remove remarks from here)
        required_fields = [
            "agent_name", "agent_mobile", "agent_email", "agent_address",
            "agent_city", "agent_state", "agent_country", "agent_pincode", 
            "agent_geolocation", "agent_category", "agent_businessname"
        ]

        missing_fields = [field for field in required_fields if field not in agent_data]

        if missing_fields:
            return {"message": f"Missing required fields: {', '.join(missing_fields)}"}

        # Set default values
        agent_data["active_flag"] = 0  # Default active_flag to 0

        logger.info("Creating new agent...")

        # Create the new agent
        new_agent = Agent(**agent_data)
        db.add(new_agent)
        db.commit()
        db.refresh(new_agent)

        # Return the created agent details
        return {
            "message": "agent created successfully",
            "agent_id": new_agent.agent_id,
            "agent_name": new_agent.agent_name,
            "agent_mobile": new_agent.agent_mobile,
            "agent_email": new_agent.agent_email,
            "agent_address": new_agent.agent_address,
            "agent_city": new_agent.agent_city,
            "agent_state": new_agent.agent_state,
            "agent_country": new_agent.agent_country,
            "agent_pincode": new_agent.agent_pincode,
            "agent_geolocation": new_agent.agent_geolocation,
            "agent_category": new_agent.agent_category,
            "agent_businessname": new_agent.agent_businessname,
            "active_flag": new_agent.active_flag,
            "remarks": new_agent.remarks,
            **{key: getattr(new_agent, key) for key in agent_data.keys()},
        }

    except IntegrityError as e:
        logger.error(f"IntegrityError: {str(e)}")
        db.rollback()
        return {"message": "Database error occurred. Please check input data."}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        db.rollback()
        return {"message": f"Error creating agent: {str(e)}"}





def update_agent_service(db: Session, agent_id: int, agent_data: dict) -> dict:
    """Business logic for updating a agent's details based on agent ID."""
    try:
        # Step 1: Check if the agent exists based on agent_id
        existing_agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
        if not existing_agent:
            return {"message": "No agents found"}  # Return message if no agent is found

        # Step 2: Update agent details with the provided data
        for field, value in agent_data.items():
            if hasattr(existing_agent, field) and value is not None:
                setattr(existing_agent, field, value)

        # Commit changes to the database
        db.commit()
        db.refresh(existing_agent)

        # Return the updated agent details
        return {
            "agent_id": existing_agent.agent_id,
            "agent_name": existing_agent.agent_name,
            "agent_email": existing_agent.agent_email,
            "agent_mobile": existing_agent.agent_mobile,
            "agent_address": existing_agent.agent_address,
            "agent_city": existing_agent.agent_city,
            "agent_state": existing_agent.agent_state,
            "agent_country": existing_agent.agent_country,
            "agent_pincode": existing_agent.agent_pincode,
            "agent_geolocation": existing_agent.agent_geolocation,
            "active_flag": existing_agent.active_flag,
            "remarks": existing_agent.remarks,
        }

    except IntegrityError as e:
        db.rollback()
        return {"message": f"Database error: {str(e)}"}
    except Exception as e:
        db.rollback()
        return {"message": f"Error updating agent: {str(e)}"}


def suspend_or_activate_agent(db: Session, agent_mobile: str, active_flag: int, remarks: str) -> dict:
    """
    Suspend or activate a agent based on the active_flag input.

    Args:
        db (Session): Database session.
        agent_mobile (str): Mobile number of the agent.
        active_flag (int): 1 for activate, 2 for suspend.
        remarks (str): Remarks or notes for the action.

    Returns:
        dict: Updated agent details or error message.
    """
    from app.crud.agents import get_agent_by_mobile, update_agent_status
    try:
        # Fetch the agent by mobile
        existing_agent = get_agent_by_mobile(db, agent_mobile)
        if not existing_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No agent found with the provided mobile number."
            )

        # Update the agent's active_flag and remarks
        update_agent_status(db, existing_agent, active_flag, remarks)
        db.refresh(existing_agent)

        # Return the updated agent details
        return {
            'message': 'agent status updated successfully.',
            "agent": {
                "agent_id": existing_agent.agent_id,
                "agent_name": existing_agent.agent_name,
                "agent_email": existing_agent.agent_email,
                "agent_mobile": existing_agent.agent_mobile,
                "agent_address": existing_agent.agent_address,
                "agent_city": existing_agent.agent_city,
                "agent_state": existing_agent.agent_state,
                "agent_country": existing_agent.agent_country,
                "agent_pincode": existing_agent.agent_pincode,
                "agent_geolocation": existing_agent.agent_geolocation,
                "active_flag": active_flag,
                "remarks": remarks
            }
        }

    except HTTPException as http_exc:
        # Re-raise HTTP exceptions
        raise http_exc
    except Exception as e:
        # Rollback the transaction on error
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating agent status: {str(e)}"
        )


def get_agent_profile(db: Session, agent_mobile: str) -> dict:
    """Retrieve the profile of a agent based on their mobile number."""
    from app.crud.agents import get_agent_by_mobile
    agent = get_agent_by_mobile(db, agent_mobile)
    if agent:
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
            "active_flag": agent.active_flag,
            "remarks": agent.remarks
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="agent not found"
        )

def get_agents_profile_list(db: Session) -> list:
    """Retrieve a list of all agent profiles."""
    try:
        # Get the list of all agents from the database without filters
        agents = db.query(Agent).all()  # This will retrieve all agents
        
        # Map the agents to a list of dictionaries (profiles)
        agent_profiles = [
            {
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
                "active_flag": agent.active_flag,
                "remarks": agent.remarks
            }
            for agent in agents
        ]
        return agent_profiles
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving agent profiles: {str(e)}"
        )


def soft_delete_agent_service(db: Session, agent_id: int):
    """Service layer function to soft delete a agent."""
    from app.crud.agents import soft_delete_agent_crud
    try:
        # Call the CRUD function to soft delete the agent
        deleted_agent = soft_delete_agent_crud(db, agent_id)
        return deleted_agent
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while trying to soft delete the agent: {str(e)}"
        )