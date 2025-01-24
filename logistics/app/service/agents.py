from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.agents import Agent, AgentCredential
from app.models.bookings import Bookings
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.utils import check_existing_agent_by_mobile, hash_password, process_credentials
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

        # Check if agent already exists using mobile number
        if check_existing_agent_by_mobile(db, agent_data["agent_mobile"]):
            return {"message": "Agent already exists"}

        # Set default values
        agent_data["active_flag"] = 0  # Default active_flag to 0
        agent_data["verification_status"] = "Pending"  # Default verification status to 'Pending'

        logger.info("Processing credentials...")
        credentials_data = process_credentials(agent_data)

        logger.info("Creating new agent...")
        # Create the new agent
        new_agent = Agent(**agent_data)
        db.add(new_agent)
        db.commit()
        db.refresh(new_agent)

        # Create associated credentials if provided
        if credentials_data["email_id"] and credentials_data["password"]:
            credentials_data["password"] = hash_password(credentials_data["password"])
            credentials_data["agent_id"] = new_agent.agent_id

            logger.info("Creating agent credentials...")
            new_credential = AgentCredential(**credentials_data)
            db.add(new_credential)
            db.commit()
            db.refresh(new_credential)

        # Return the created agent details
        return {
            "message": "Agent created successfully",
            "agent_id": new_agent.agent_id,
            "agent_name": new_agent.agent_name,
            "agent_mobile": new_agent.agent_mobile,
            **{key: getattr(new_agent, key) for key in agent_data.keys()},
            "verification_status": new_agent.verification_status,
            "credential_details": {
                "email_id": credentials_data.get("email_id"),
                "agent_credential_id": new_credential.agent_credential_id if credentials_data["email_id"] else None
            },
            
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

        # Step 2: Exclude fields that shouldn't be updated (verification_status, category, notes)
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
        # Step 1: Validate the active flag value
        if active_flag not in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid active flag value. Use 1 (Activate) or 2 (Suspend)."
            )

        # Step 2: Fetch the agent by mobile
        existing_agent = get_agent_by_mobile(db, agent_mobile)
        if not existing_agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No agent found with the provided mobile number."
            )

        # Step 3: Update the agent's status
        update_agent_status(db, existing_agent, active_flag, remarks)
        db.refresh(existing_agent)

        # Step 4: Dynamically set verification status
        verification_status = "Verified" if active_flag == 1 else "Suspend"

        # Step 5: Return the updated agent details
        return {
            'message': 'Agent status updated successfully.',
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
                "agent_category": existing_agent.agent_category.value,
                "agent_businessname": existing_agent.agent_businessname,
                "tax_id": existing_agent.tax_id,
                "active_flag": active_flag,
                "verification_status": verification_status,
                "remarks": existing_agent.remarks
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



def verify_agent_service(db: Session, agent_mobile: str, verification_status: str) -> dict:
    """
    Verify the agent and update their verification status and active flag.

    Args:
        db (Session): Database session.
        agent_mobile (str): Mobile number of the agent.
        verification_status (str): Verification status ('Verified' or 'Not Verified').

    Returns:
        dict: Updated agent details or error message.
    """
    try:
        # Step 1: Retrieve the agent based on the mobile number
        existing_agent = db.query(Agent).filter(Agent.agent_mobile == agent_mobile).first()

        if not existing_agent:
            # Step 2: Return message if the agent is not found
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No agent found with the provided mobile number."
            )

        # Step 3: Update verification status and active flag
        if verification_status.lower() == "verified":
            existing_agent.verification_status = "Verified"
            existing_agent.active_flag = 1  # Activate the agent
        else:
            existing_agent.verification_status = verification_status
            existing_agent.active_flag = 0  # Optional: Deactivate or leave unchanged

        # Commit the changes to the database
        db.commit()
        db.refresh(existing_agent)

        # Step 4: Return the updated agent details
        return {
            "message": "Agent verification status updated successfully.",
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
                "agent_businessname": existing_agent.agent_businessname,
                "tax_id": existing_agent.tax_id,
                "verification_status": existing_agent.verification_status,
                "active_flag": existing_agent.active_flag,
            },
        }
    except Exception as e:
        # Rollback the transaction in case of an unexpected error
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying agent: {str(e)}"
        )


def get_agent_profile(db: Session, agent_mobile: str) -> dict:
    """Retrieve the profile of an agent based on their mobile number."""
    from app.crud.agents import get_agent_by_mobile
    agent = get_agent_by_mobile(db, agent_mobile)
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


def get_all_agents_with_booking_list(db: Session) -> list:
    """
    Retrieve all agents with their booking list summaries.
    """
    try:
        agents = db.query(Agent).all()
        if not agents:
            raise HTTPException(status_code=404, detail="No agents found")

        agent_list = []
        for agent in agents:
            bookings = db.query(Bookings).filter(Bookings.agent_id == agent.agent_id).all()
            booking_summary = [
                {
                    "booking_id": booking.booking_id,
                    "from_city": booking.from_city,
                    "from_pincode": booking.from_pincode,
                    "to_city": booking.to_city,
                    "to_pincode": booking.to_pincode,
                    "status": booking.booking_status,
                    "action": f"View details of Booking {booking.booking_id}",
                }
                for booking in bookings
            ]
            response = {
                "agent_id": agent.agent_id,
                "agent_name": agent.agent_name,
                "agent_mobile": agent.agent_mobile,
                "agent_email": agent.agent_email,
                "agent_address": agent.agent_address,
                "agent_city": agent.agent_city,
                "agent_state": agent.agent_state,
                "agent_country": agent.agent_country,
                "agent_pincode": agent.agent_pincode,
                "agent_geolocation": agent.agent_geolocation,
                "agent_businessname": agent.agent_businessname,
                "tax_id": agent.tax_id,
                "verification_status": agent.verification_status,
                "active_flag": agent.active_flag,
                "agent_category": agent.agent_category,
                "bookings": booking_summary
            }
            agent_list.append(response)

        return agent_list

    except Exception as e:
        logging.error(f"Error fetching agent list with booking summaries: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching agent list: {str(e)}")



def get_agent_with_booking_details(db: Session, agent_id: int, booking_id: int):
    from app.models.bookings import BookingItem  # Import BookingItem
    try:
        # Query the booking with the specified agent_id and booking_id
        booking = db.query(Bookings).filter(Bookings.agent_id == agent_id, Bookings.booking_id == booking_id).first()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        # Retrieve the agent details
        agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")


        # Prepare the booking response with agents and booking details
        booking_response = {
            "agent_name": agent.agent_name,
            "agent_mobile": agent.agent_mobile,
            "agent_email": agent.agent_email,
            "agent_address": agent.agent_address,
            "agent_city": agent.agent_city,
            "agent_state": agent.agent_state,
            "agent_country": agent.agent_country,
            "agent_pincode": agent.agent_pincode,
            "booking_id": booking.booking_id,
            "from_address": booking.from_address,
            "from_city": booking.from_city,
            "from_pincode": booking.from_pincode,
            "to_address": booking.to_address,
            "to_city": booking.to_city,
            "to_pincode": booking.to_pincode,
            "package_details": {
                "no_of_packages": booking.package_count,
                "pickup_date": booking.pickup_date,
                "pickup_time": booking.pickup_time,
                "estimated_delivery_date": booking.estimated_delivery_date
            },
            "item_details": [
                {
                    "item_id": item.item_id,
                    "booking_id": item.booking_id,
                    "weight": item.weight,
                    "length": item.length,
                    "width": item.width,
                    "height": item.height,
                    "package_type": item.package_type.name,  # Assuming package_type is an enum
                    "cost": item.cost,
                    "ratings": item.rating,
                }
                for item in db.query(BookingItem).filter(BookingItem.booking_id == booking.booking_id).all()
            ],
        }

        return booking_response

    except Exception as e:
        logging.error(f"Error retrieving booking details for agent {agent_id} and booking {booking_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def get_agent_booking_list(agent_id: int, db: Session):
    from app.crud.agents import get_agents_and_bookings
    from app.schemas.agents import AgentBookingListResponse
    from app.schemas.bookings import BookingSummary

    try:
        # Fetch agent and bookings
        agent, bookings = get_agents_and_bookings(db, agent_id)

        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        # Construct booking summary
        booking_summary = [
            BookingSummary(
                booking_id=booking.booking_id,
                from_city=booking.from_city,
                from_pincode=booking.from_pincode,
                to_city=booking.to_city,
                to_pincode=booking.to_pincode,
                status=booking.booking_status,
                action=f"View details of Booking {booking.booking_id}",
            )
            for booking in bookings
        ]

        # Construct response
        return AgentBookingListResponse(
            agent_id=agent.agent_id,
            agent_name=agent.agent_name,
            agent_mobile=agent.agent_mobile,
            agent_email=agent.agent_email,  # Ensure this matches the schema
            agent_address=agent.agent_address,
            agent_city=agent.agent_city,
            agent_state=agent.agent_state,
            agent_country=agent.agent_country,
            agent_pincode=agent.agent_pincode,
            agent_geolocation=agent.agent_geolocation,
            tax_id=agent.tax_id,
            agent_businessname=agent.agent_businessname,
            bookings=booking_summary,
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error fetching agent booking list: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching booking list: {str(e)}")
