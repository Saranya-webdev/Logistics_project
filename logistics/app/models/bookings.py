from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Enum, DECIMAL, Date, Time
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.enums import PickupMethod, PickupStatus, PackageType

# Booking Model
class Bookings(Base):
    __tablename__ = 'bookings'

    booking_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)  # ForeignKey to Customer
    created_by = Column(Integer, ForeignKey("users.user_id"))  # ForeignKey to the creator (User)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    from_address = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    state = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    pincode = Column(Integer, nullable=True)
    to_name = Column(String(255), nullable=False)
    to_phone_number = Column(String(255), nullable=False)
    to_email = Column(String(255), nullable=False)
    to_address = Column(String(255), nullable=False)
    to_city = Column(String(255), nullable=False)
    to_state = Column(String(255), nullable=False)
    to_country = Column(String(255), nullable=False)
    to_pincode = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    estimated_delivery_date = Column(DateTime, nullable=True)
    estimated_delivery_cost = Column(DECIMAL(10, 2), nullable=False)
    pickup_time = Column(Time, nullable=True)
    pickup_date = Column(Date, nullable=True)
    quotation_id = Column(Integer, ForeignKey('quotations.quotation_id'))
    package_count = Column(Integer, default=0)
    pickup_method = Column(Enum(PickupMethod)) 
    booking_status = Column(Enum(PickupStatus), nullable=True)

    # Relationships
    quotation = relationship('Quotations', back_populates='bookings', foreign_keys=[quotation_id])
    customer = relationship("Customer", back_populates="bookings", foreign_keys=[customer_id])
    booking_items = relationship("BookingItem", back_populates="booking")


# Booking Item Model
class BookingItem(Base):
    __tablename__ = 'booking_items'

    item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"), nullable=False)
    weight = Column(DECIMAL(10, 2), nullable=False)
    length = Column(DECIMAL(10, 2), nullable=False)
    width = Column(DECIMAL(10, 2), nullable=False)
    height = Column(DECIMAL(10, 2), nullable=False)
    package_type = Column(Enum(PackageType), nullable=False, name='package_type')
    cost = Column(DECIMAL(10, 2), nullable=False)
    booking = relationship("Bookings", back_populates="booking_items")
