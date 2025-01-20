# models/users.py
from sqlalchemy import Integer, String, Column, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.models.base import Base

# User Role Enum
class UserRole(str, enum.Enum):
    logistic_company = 'logistic_company'
    agent = 'agent'
    employee = 'employee'
    customer = 'customer'

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    mobile = Column(String(15))
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    extend_existing=True

    # Relationship back to AddressBook
    address_books = relationship("AddressBook", back_populates="user")

    class Config:
        orm_mode = True
