from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.sql import func
from app.models.base import Base
from sqlalchemy.orm import relationship
from app.models.enums import Category, VerificationStatus

    

# Agent Model
class Agent(Base):
    __tablename__ = 'agent'
    __table_args__ = {'extend_existing': True}

    agent_id = Column(Integer, primary_key=True, autoincrement=True)
    agent_name = Column(String(255), nullable=False)
    agent_mobile = Column(String(15))
    agent_email = Column(String(255), nullable=False, unique=True)
    agent_address = Column(String(255), nullable=False)
    agent_city = Column(String(255), nullable=False)
    agent_state = Column(String(255), nullable=False)
    agent_country = Column(String(255), nullable=False)
    agent_pincode = Column(String(255), nullable=True)
    agent_geolocation = Column(String(255), nullable=False)
    agent_category = Column(
        Enum(Category, name="customer_category_enum"), nullable=False
    )
    agent_businessname = Column(String(255), nullable=False)
    tax_id = Column(String(255), nullable=False)
    remarks = Column(String(255), nullable=True)
    verification_status = Column(Enum(VerificationStatus), nullable=False, default=VerificationStatus.none)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    active_flag = Column(Integer, default=1)
    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    # created_by = Column(Integer, ForeignKey("user.user_id"))
    # updated_by = Column(Integer, ForeignKey("user.user_id"))

    agent_credentials = relationship("AgentCredential", back_populates="agent", cascade="all, delete-orphan")    

    class Config:
        orm_mode = True

    
class AgentCredential(Base):
    __tablename__ = 'agent_credential'
    __table_args__ = {'extend_existing': True}

    agent_credential_id = Column(Integer, primary_key=True)
    email_id = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    agent_id = Column(Integer, ForeignKey("agent.agent_id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    # created_by = Column(Integer, ForeignKey("user.user_id"))
    # updated_by = Column(Integer, ForeignKey("user.user_id"))
    active_flag = Column(Integer, default=1)

    agent = relationship("Agent", back_populates="agent_credentials")

    class Config:
        orm_mode = True


    
