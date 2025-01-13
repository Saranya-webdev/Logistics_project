from sqlalchemy import Integer, String, Column, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
# from app.databases.mysqldb import Base
import enum
from app.models.bookings import Bookings
from app.models.quotations import Quotations
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
    bookings = relationship("Bookings", back_populates="user", foreign_keys=[Bookings.user_id])
    quotations = relationship("Quotations", back_populates="user", foreign_keys=[Quotations.user_id])
    created_bookings = relationship("Bookings", back_populates="creator", foreign_keys=[Bookings.created_by])
    created_quotations = relationship("Quotations", back_populates="created_by_user", foreign_keys=[Quotations.created_by])
    address_books = relationship("AddressBook", back_populates="user")
