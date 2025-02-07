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
    email_id = Column(String(255), nullable=False)  # Removed unique=True to allow multiple addresses with same email
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
    # created_by = Column(Integer, ForeignKey("user.user_id"))
    # updated_by = Column(Integer, ForeignKey("user.user_id"))

    # Relationship back to Customer
    customer = relationship(
        "Customer", 
        back_populates="address_books", 
        primaryjoin="AddressBook.customer_id == Customer.customer_id"
    )

    # Relationships with Bookings
    # bookings_from = relationship("Bookings", foreign_keys="[Bookings.from_address_id]", back_populates="from_address", overlaps="from_address")
    # bookings_to = relationship("Bookings", foreign_keys="[Bookings.to_address_id]", back_populates="to_address", overlaps="to_address")

    class Config:
        orm_mode = True
