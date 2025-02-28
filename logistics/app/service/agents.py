from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.agents import Agent, AgentCredential
from app.models.enums import VerificationStatus
from app.utils.utils import check_existing_by_email,check_existing_by_id_and_email,get_credential_by_id
<<<<<<< HEAD
from app.crud.agents import create_agent_crud, update_agent_crud, suspend_or_active_agent_crud, verify_agent_crud, get_agent_profile_crud, get_all_agents_crud,create_agent_credential,update_agent_password_crud, get_bookings_by_agent_crud
import logging
import bcrypt
from datetime import date
=======
from app.crud.agents import create_agent_crud, update_agent_crud, suspend_or_active_agent_crud, verify_agent_crud, get_agent_profile_crud, get_all_agents_crud,create_agent_credential,update_agent_password_crud
import logging
import bcrypt
>>>>>>> origin/main

logger = logging.getLogger(__name__)

def create_agent_service(db: Session, agent_data: dict) -> dict:
    """Business logic for creating an agent."""
    try:
        # Log validation process
        logger.info("Validating if the agent already exists...")

        # Check if agent already exists using email
        if check_existing_by_email(db, Agent, "agent_email", agent_data["agent_email"]):
            return {"message": "Agent already exists"}

        # Set default values
        agent_data["active_flag"] = 0  # Default active_flag to 0
        agent_data["verification_status"] = "Pending"  # Default verification status to 'Pending'

        logger.info("Creating new agent...")
        # Call CRUD to create the new agent in DB
        new_agent = create_agent_crud(db, agent_data)

        # Return the created agent details
        return {
            "message": "Agent created successfully",
            "agent_id": new_agent.agent_id,
            "agent_name": new_agent.agent_name,
            "agent_mobile": new_agent.agent_mobile,
            **{key: getattr(new_agent, key) for key in agent_data.keys()},
            "verification_status": new_agent.verification_status,
        }

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        db.rollback()
        return {"message": f"Error creating agent: {str(e)}"}
    

def create_agent_credential_service(db: Session, agent_id: int, agent_email: str, password: str):
    """Business logic for creating agent credentials"""
    try:
        #  Pass the correct model class (Agent) instead of an undefined variable
        agent = check_existing_by_id_and_email(db, Agent, "agent_id", "agent_email", agent_id, agent_email)
        
        if not agent:
            print("Agent ID and Email do not match. Cannot create credentials.")
            return None  # Or raise an exception

        #  Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Call the correct function to create the agent credentials
        return create_agent_credential(db, agent.agent_id, agent.agent_email, hashed_password)

    except Exception as e:
        print(f"Error in service layer: {e}")
        return None  
    

def update_agent_password_service(db: Session, agent_id: int, new_password: str):
    """Business logic for updating an associate's password."""
    try:
        # Fetch the credential using the generic function
        credential = get_credential_by_id(db, AgentCredential, "agent_id", agent_id)

        if not credential:
            raise ValueError("Associate credential not found.")

        # Hash the new password securely
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Call CRUD function with hashed password
        return update_agent_password_crud(db, credential, hashed_password)
    except ValueError as e:
        raise ValueError(str(e))  # Pass custom error
    except Exception as e:
        raise Exception(f"Service error while updating password: {e}")    



def get_agent_profile(db: Session, agent_email: str) -> dict:
    """
    Retrieve the profile of an agent based on their email.
    """
    try:
        # Call the CRUD function to fetch the agent
        agent = get_agent_profile_crud(db, agent_email)

        # If no agent is found, raise a 404 exception
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )

        # Format the response with the agent's profile details
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
    except HTTPException as http_exc:
        # Handle HTTP-specific exceptions
        raise http_exc
    except Exception as e:
        # Handle unexpected exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving the agent profile: {str(e)}"
        )


def get_all_agents_profile(db: Session) -> list:
    """
    Retrieve the profiles of all agents.
    """
    try:
        # Call the CRUD function to fetch all agents
        agents = get_all_agents_crud(db)

        # If no agents are found, raise a 404 exception
        if not agents:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No agents found"
            )

        # Prepare the response as a list of dictionaries
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
    except Exception as e:
        # Handle unexpected exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving agents: {str(e)}"
        )
    

<<<<<<< HEAD
def get_bookings_by_agent_service(db, agent_email):
    """
    Retrieves all bookings placed by a specific agent and formats them.
    """
    try:
        bookings = get_bookings_by_agent_crud(db, agent_email)

        if not bookings:
            return {  
                "agent_email": agent_email,
                "message": "No bookings found for this agent",
                "bookings": []
            }

        return {
            "agent_email": agent_email,
            "bookings": [
                {
                    "booking_id": booking.booking_id,
                    "customer_id": booking.customer_id,
                    "booking_by": booking.booking_by,
                    "from_city": booking.from_city,
                    "from_pincode": booking.from_pincode,
                    "to_city": booking.to_city,
                    "to_pincode": booking.to_pincode,
                    "carrier_plan": booking.carrier_plan,
                    "carrier_name": booking.carrier_name,
                    "pickup_date": booking.pickup_date.strftime("%Y-%m-%d"),
                    "package_count": str(booking.package_count),
                    "total_cost":  str(booking.total_cost),
                    "booking_status": booking.booking_status,
                    "booking_items": [
                        {
                            "item_id": item.item_id,
                            "item_length": item.item_length,
                            "item_weight": item.item_weight,
                            "item_width":item.item_width,
                            "item_height": item.item_height,
                            "package_type": item.package_type,
                        }
                        for item in booking.booking_items
                    ],
                }
                for booking in bookings
            ],
        }

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logging.error(f"Error retrieving bookings by agent {agent_email}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    

=======
>>>>>>> origin/main
def update_agent_service(db: Session, agent_data: dict) -> dict:
    """Business logic for updating an agent's details based on agent email."""
    try:
        # Step 1: Check if the agent exists based on email
        existing_agent = check_existing_by_email(db, Agent, "agent_email", agent_data["agent_email"])
        if not existing_agent:
            return {"message": "No agents found with the given email."}  # Return message if no agent is found

        # Step 2: Exclude fields that shouldn't be updated
        fields_to_exclude = ["verification_status", "agent_category", "notes"]
        filtered_data = {key: value for key, value in agent_data.items() if key not in fields_to_exclude and value is not None}

        # Step 3: Update the agent's details (without modifying the agent_email)
        updated_agent = update_agent_crud(db, existing_agent, filtered_data)

        if not updated_agent:
            return {"message": "Error updating agent details."}

        # Return the updated agent details (excluding email modification)
        return {
            "agent_id": updated_agent.agent_id,
            "agent_name": updated_agent.agent_name,
            "agent_email": updated_agent.agent_email,  # Keep original email
            "agent_mobile": updated_agent.agent_mobile,
            "agent_address": updated_agent.agent_address,
            "agent_city": updated_agent.agent_city,
            "agent_state": updated_agent.agent_state,
            "agent_country": updated_agent.agent_country,
            "agent_pincode": updated_agent.agent_pincode,
            "agent_geolocation": updated_agent.agent_geolocation,
            "agent_businessname": updated_agent.agent_businessname,
            "tax_id": updated_agent.tax_id,
            "active_flag": updated_agent.active_flag,
            "verification_status": updated_agent.verification_status,  # Include verification status if needed
            "agent_category": updated_agent.agent_category  # Include agent category if needed
        }

    except Exception as e:
        logger.error(f"Error in updating agent: {str(e)}")
        db.rollback()
        return {"message": f"Error updating agent: {str(e)}"}




def suspend_or_activate_agent(db: Session, agent_email: str, active_flag: int, remarks: str) -> dict:
    """
    Suspend or activate an agent based on the active_flag input.

    Args:
        db (Session): Database session.
        agent_email (str): email of the agent.
        active_flag (int): 1 for activate, 2 for suspend.
        remarks (str): Remarks or notes for the action.

    Returns:
        dict: Updated agent details or error message.
    """
    try:
        # Step 1: Validate the active flag value
        if active_flag not in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid active flag value. Use 1 (Activate) or 2 (Suspend)."
            )

        # Step 2: Check if the agent exists using utility function
        existing_agent = check_existing_by_email(db, Agent, "agent_email", agent_email)
        if not existing_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No agent found with the provided email."
            )

        # Step 3: Call the CRUD function to update the agent
        updated_agent = suspend_or_active_agent_crud(db, agent_email, active_flag, remarks)

        if not updated_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No agent found with the provided email."
            )

        # Step 4: Return the updated agent details directly as a dictionary
        return {
            "message": "Agent status updated successfully.",
            "agent": {
                "agent_id": updated_agent.agent_id,
                "agent_name": updated_agent.agent_name,
                "agent_email": updated_agent.agent_email,
                "agent_mobile": updated_agent.agent_mobile,
                "active_flag": updated_agent.active_flag,
                "remarks": updated_agent.remarks,
                "verification_status": updated_agent.verification_status  # Handle this optional field properly
            }
        }

    except HTTPException as http_exc:
        # Raise HTTP exceptions
        raise http_exc
    except Exception as e:
        # Handle general exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating agent status: {str(e)}"
        )




def verify_agent_service(db: Session, agent_email: str, verification_status: str) -> dict:
    """
    Service method to verify the agent and update their verification status and active flag.
    """
    try:
        # Ensure verification_status is treated as a string
        verification_status_value = verification_status if isinstance(verification_status, str) else verification_status.value

        # Now compare verification_status with Enum's value
        if verification_status_value.lower() == VerificationStatus.verified.value:
            active_flag = 1
        else:
            active_flag = 0

        # Call the CRUD function to update the agent's status
        updated_agent = verify_agent_crud(db, agent_email, verification_status, active_flag)

        if not updated_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No agent found with the provided email."
            )

        # Return the response with correct structure
        return {

                "agent_id": updated_agent.agent_id,
                "agent_name": updated_agent.agent_name,
                "agent_email": updated_agent.agent_email,
                "agent_mobile": updated_agent.agent_mobile,
                "verification_status": updated_agent.verification_status.value,  # Convert Enum to string
                "active_flag": updated_agent.active_flag,
                "remarks": updated_agent.remarks,
            }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying agent: {str(e)}"
        )
