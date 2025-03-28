from sqlalchemy import Integer, String, Column, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base
from sqlalchemy.orm import relationship
from app.models.bookings import Bookings

# Address Book Model
class AddressBook(Base):
    __tablename__ = "address_books"
    __table_args__ = {'extend_existing': True}

    address_id = Column(Integer, primary_key=True, autoincrement=True)
    address_name = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    mobile =  Column(String(15))
    email_id = Column(String(255), nullable=False) 
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    pincode = Column(String(20), nullable=False)
    company_name = Column(String(255), nullable=False)
    address_type = Column(String(255), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)
    
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # Relationship back to Customer
    customer = relationship(
        "Customer", 
        back_populates="address_books", 
        primaryjoin="AddressBook.customer_id == Customer.customer_id"
    )

    class Config:
        orm_mode = True
