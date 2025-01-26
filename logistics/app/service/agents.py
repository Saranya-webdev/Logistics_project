from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.agents import Agent
from app.utils import check_existing_by_email
import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

def create_agent_service(db: Session, agent_data: dict) -> dict:
    """Business logic for creating an agent."""
    try:
        # Log validation process
        logger.info("Validating if the agent already exists...")

        # Check if agent already exists using mobile number
        if check_existing_by_email(db,Agent, "agent_email", agent_data["agent_email"]):
            return {"message": "Agent already exists"}

        # Set default values
        agent_data["active_flag"] = 0  # Default active_flag to 0
        agent_data["verification_status"] = "Pending"  # Default verification status to 'Pending'

        logger.info("Creating new agent...")
        # Create the new agent
        new_agent = Agent(**agent_data)
        db.add(new_agent)
        db.commit()
        db.refresh(new_agent)

        # Return the created agent details
        return {
            "message": "Agent created successfully",
            "agent_id": new_agent.agent_id,
            "agent_name": new_agent.agent_name,
            "agent_mobile": new_agent.agent_mobile,
            **{key: getattr(new_agent, key) for key in agent_data.keys()},
            "verification_status": new_agent.verification_status,
        }

    except IntegrityError as e:
        logger.error(f"IntegrityError: {str(e)}")
        db.rollback()
        return {"message": "Database error occurred. Please check input data."}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        db.rollback()
        return {"message": f"Error creating agent: {str(e)}"}


def update_agent_service(db: Session, agent_data: dict) -> dict:
    """Business logic for updating an agent's details based on agent email."""
    try:
        # Step 1: Check if the agent exists based on email
        existing_agent = db.query(Agent).filter(Agent.agent_email == agent_data["agent_email"]).first()
        if not existing_agent:
            return {"message": "No agents found"}  # Return message if no agent is found

        # Step 2: Exclude fields that shouldn't be updated
        fields_to_exclude = ["verification_status", "agent_category", "notes"]
        filtered_data = {key: value for key, value in agent_data.items() if key not in fields_to_exclude and value is not None}

        # Step 3: Update agent details with the filtered data
        for field, value in filtered_data.items():
            if hasattr(existing_agent, field):
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
            "agent_businessname": existing_agent.agent_businessname,
            "tax_id": existing_agent.tax_id,
            "active_flag": existing_agent.active_flag,
        }

    except IntegrityError as e:
        db.rollback()
        return {"message": f"Database error: {str(e)}"}
    except Exception as e:
        db.rollback()
        return {"message": f"Error updating agent: {str(e)}"}


def suspend_or_activate_agent(db: Session, agent_mobile: str, active_flag: int, remarks: str) -> dict:
    """
    Suspend or activate an agent based on the active_flag input.
    """
    try:
        # Step 1: Validate the active flag value
        if active_flag not in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid active flag value. Use 1 (Activate) or 2 (Suspend)."
            )

        # Step 2: Fetch the agent by mobile
        existing_agent = db.query(Agent).filter(Agent.agent_mobile == agent_mobile).first()
        if not existing_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No agent found with the provided mobile number."
            )

        # Step 3: Update the agent's status
        existing_agent.active_flag = active_flag
        existing_agent.remarks = remarks
        db.commit()
        db.refresh(existing_agent)

        # Step 4: Set verification status dynamically
        verification_status = "Verified" if active_flag == 1 else "Suspended"

        # Step 5: Return the updated agent details
        return {
            'message': 'Agent status updated successfully.',
            "agent": {
                "agent_id": existing_agent.agent_id,
                "agent_name": existing_agent.agent_name,
                "agent_email": existing_agent.agent_email,
                "agent_mobile": existing_agent.agent_mobile,
                "active_flag": active_flag,
                "verification_status": verification_status,
                "remarks": existing_agent.remarks
            }
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating agent status: {str(e)}"
        )


def verify_agent_service(db: Session, agent_mobile: str, verification_status: str) -> dict:
    """
    Verify the agent and update their verification status and active flag.
    """
    try:
        # Step 1: Retrieve the agent based on the mobile number
        existing_agent = db.query(Agent).filter(Agent.agent_mobile == agent_mobile).first()

        if not existing_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No agent found with the provided mobile number."
            )

        # Step 2: Update verification status and active flag
        if verification_status.lower() == "verified":
            existing_agent.verification_status = "Verified"
            existing_agent.active_flag = 1  # Activate the agent
        else:
            existing_agent.verification_status = verification_status
            existing_agent.active_flag = 0

        # Commit the changes to the database
        db.commit()
        db.refresh(existing_agent)

        # Step 3: Return the updated agent details
        return {
            "message": "Agent verification status updated successfully.",
            "agent": {
                "agent_id": existing_agent.agent_id,
                "agent_name": existing_agent.agent_name,
                "agent_email": existing_agent.agent_email,
                "agent_mobile": existing_agent.agent_mobile,
                "verification_status": existing_agent.verification_status,
                "active_flag": existing_agent.active_flag,
            },
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying agent: {str(e)}"
        )


def get_agent_profile(db: Session, agent_email: str) -> dict:
    """Retrieve the profile of an agent based on their email."""
    agent = db.query(Agent).filter(Agent.agent_email == agent_email).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

    response = {
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
        "verification_status": agent.verification_status,
    }
    return response


def get_all_agents_profile(db: Session) -> list:
    """Retrieve the profiles of all agents."""
    agents = db.query(Agent).all()
    if not agents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No agents found")

    # Preparing the response as a list of dictionaries
    response = [
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
            "agent_businessname": agent.agent_businessname,
            "tax_id": agent.tax_id,
            "verification_status": agent.verification_status,
        }
        for agent in agents
    ]
    return response
