from sqlalchemy import Enum, Integer, String, Column, DateTime
import enum
from sqlalchemy.sql import func
from app.database import Base

# Enums for customer model
class CustomerCategory(str, enum.Enum):
    individual = "individual"
    company = "company"
    business = "business"
    customs_agent = "customs_agent"
    carrier = "carrier"

class CustomerType(str, enum.Enum):
    personal = "personal"
    business = "business"

# Customer Model
class Customer(Base):
    __tablename__ = 'customers' 

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    mobile = Column(Integer, nullable=True)
    address = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    pincode = Column(Integer, nullable=False)
    country = Column(String(255), nullable=False)
    categories = Column(Enum(CustomerCategory), nullable=False)
    type = Column(Enum(CustomerType), nullable=False)
    taxid = Column(String(255), nullable=False)
    licensenumber = Column(String(255), nullable=False)
    designation = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    createddate = Column(DateTime, nullable=False, default=func.now())
    updateddate = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    class Config:
        orm_mode = True

