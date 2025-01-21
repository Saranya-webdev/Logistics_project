from sqlalchemy import Integer, String, Column, DateTime, ForeignKey,Boolean, DECIMAL
from sqlalchemy.sql import func
from app.models.base import Base
from sqlalchemy.orm import relationship
from app.models.bookings import Booking
from enum import Enum

class AgentType(str,Enum):
    tier_1 = "Tier 1"
    tier_2 = "Tier 2"
    tier_3 = "Tier 3"

class AgentCategory(str, Enum):
    individual = "Individual"
    corporate = "Corporate"


# Agent Model
class Agent(Base):
    __tablename__ = 'agent'

    agent_id = Column(Integer, primary_key=True)
    agent_name = Column(String(255), nullable=False)
    agent_mobile = Column(String(15))
    agent_email = Column(String(255), nullable=False, unique=True)
    agent_address = Column(String(255), nullable=False)
    agent_city = Column(String(255), nullable=False)
    agent_state = Column(String(255), nullable=False)
    agent_country = Column(String(255), nullable=False)
    agent_pincode = Column(String(255), nullable=True)
    agent_geolocation = Column(String(255), nullable=False)
    agent_type = Column(Enum(AgentType), nullable=True)
    agent_category = Column(Enum(AgentCategory), nullable=True)
    notes = Column(String(255))
    verification_status = Column(String(255))
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    # created_by = Column(Integer, ForeignKey("user.user_id"))
    # updated_by = Column(Integer, ForeignKey("user.user_id"))
    is_active = Column(Boolean, default=True, comment="Indicates if the agent is active or not")

    bookings = relationship("Bookings", back_populates="agent")

    class Config:
        orm_mode = True


class AgentBusiness(Base):
    __tablename__ = 'agent_business' 

    business_id = Column(Integer, primary_key=True)
    tax_id = Column(String(255), nullable=False)
    license_number = Column(String(255), nullable=False)
    designation = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    agent_id = Column(Integer, ForeignKey("agent.agent_id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    # created_by = Column(Integer, ForeignKey("user.user_id"))
    # updated_by = Column(Integer, ForeignKey("user.user_id"))
    is_active = Column(Boolean, default=True, comment="Indicates if the agent is active or not")

    class Config:
        orm_mode = True

    
class AgentCredential(Base):
    __tablename__ = 'agent_credential'

    agent_credential_id = Column(Integer, primary_key=True)
    email_id = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    # created_by = Column(Integer, ForeignKey("user.user_id"))
    # updated_by = Column(Integer, ForeignKey("user.user_id"))
    is_active = Column(Boolean, default=True, comment="Indicates if the agent is active or not")

    class Config:
        orm_mode = True

class AgentMargin(Base):
    __tablename__ = 'agent_Margin'

    agent_margin_id = Column(Integer, primary_key=True)
    agent_type = Column(Enum(AgentType), nullable=True)
    cost = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    # created_by = Column(Integer, ForeignKey("user.user_id"))
    # updated_by = Column(Integer, ForeignKey("user.user_id"))
    is_active = Column(Boolean, default=True, comment="Indicates if the agent is active or not")

    class Config:
        orm_mode = True

    
class AgentPayments(Base):
    __tablename__ = 'agent_payment'

    agent_payment_id = Column(Integer, primary_key=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_mode = Column(String(255), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    # created_by = Column(Integer, ForeignKey("user.user_id"))
    # updated_by = Column(Integer, ForeignKey("user.user_id"))
    is_active = Column(Boolean, default=True, comment="Indicates if the agent is active or not")

    booking = relationship("Bookings", back_populates="payments")

    class Config:
        orm_mode = True
    
