from sqlalchemy import Integer, String, Column, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base
from sqlalchemy.orm import relationship

# Customer Category Model
class CustomerCategory(Base):
    __tablename__ = 'customer_categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    customers = relationship("Customer", back_populates="category")  # one-to-many customers for category

# Customer Type Model
class CustomerType(Base):
    __tablename__ = 'customer_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    customers = relationship("Customer", back_populates="customer_type")

# Customer Model
class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True, index=True)  # Changed customer_id to id
    customer_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    mobile = Column(String(15))
    company = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    pincode = Column(Integer, nullable=True)
    country = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('customer_categories.id'), nullable=False)
    type_id = Column(Integer, ForeignKey('customer_types.id'), nullable=True)
    taxid = Column(String(255), nullable=False)
    licensenumber = Column(String(255), nullable=False)
    designation = Column(String(255), nullable=False)
    createddate = Column(DateTime, nullable=False, default=func.now())
    updateddate = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    
    # Relationships
    category = relationship("CustomerCategory", back_populates="customers")
    customer_type = relationship("CustomerType", back_populates="customers")
    bookings = relationship('Bookings', back_populates='customer')

    class Config:
        orm_mode = True
