from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Date, Time, DECIMAL
from sqlalchemy.sql import func
from app.models.base import Base
from sqlalchemy.orm import relationship
from app.models.enums import PickupStatus, PackageType, PaymentStatus

# Booking Model
class Bookings(Base):
    __tablename__ = 'booking'
    __table_args__ = {'extend_existing': True}

    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    from_name = Column(String(255), nullable=False)
    from_mobile = Column(String(15), nullable=False)
    from_email = Column(String(255), nullable=False)
    from_address = Column(String(255), nullable=False)
    from_city = Column(String(255), nullable=False)
    from_state = Column(String(255), nullable=False)
    from_country = Column(String(255), nullable=False)
    from_pincode = Column(String(255), nullable=True)
    
    to_name = Column(String(255), nullable=False)
    to_mobile = Column(String(15), nullable=False)
    to_email = Column(String(255), nullable=False)
    to_address = Column(String(255), nullable=False)
    to_city = Column(String(255), nullable=False)
    to_state = Column(String(255), nullable=False)
    to_country = Column(String(255), nullable=False)
    to_pincode = Column(String(255), nullable=True)

    package_count = Column(Integer, nullable=False)
    carrier_name = Column(String(255), nullable=False)
    carrier_plan = Column(String(255), nullable=False)
    est_cost = Column(DECIMAL(10, 2), nullable=False)
    est_delivery_date = Column(Date, nullable=False)
    booking_date = Column(DateTime, nullable=False, default=func.now())
    pickup_date = Column(Date, nullable=True)
    pickup_time = Column(Time, nullable=True)
    drop_time = Column(Time, nullable=True)
    drop_location = Column(String(255))
    booking_by = Column(Integer, ForeignKey("customer.customer_id"))
    total_cost = Column(DECIMAL(10, 2), nullable=False)
    booking_status = Column(SQLEnum(PickupStatus, name="pickup_status_enum"), nullable=True)
    payment_status = Column(SQLEnum(PaymentStatus, name="payment_status_enum"), default=PaymentStatus.picked, nullable=False)
    
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    quotation_id = Column(Integer, ForeignKey('quotation.quotation_id'))

    # Relationships
    customer = relationship("Customer", back_populates="bookings", foreign_keys=[customer_id])
    booking_items = relationship("BookingItem", back_populates="booking")
    customer_payments = relationship("CustomerPayments", back_populates="booking")
    quotation = relationship("Quotations", back_populates="bookings", foreign_keys=[quotation_id])
    

    class Config:
        orm_mode = True

# Booking Item Model
class BookingItem(Base):
    __tablename__ = 'booking_items'
    __table_args__ = {'extend_existing': True}

    item_id = Column(Integer, primary_key=True, autoincrement=True)
    item_length = Column(DECIMAL(10, 2), nullable=False)
    item_width = Column(DECIMAL(10, 2), nullable=False)
    item_height = Column(DECIMAL(10, 2), nullable=False)
    item_weight = Column(DECIMAL(10, 2), nullable=False)
    volumetric_weight = Column(DECIMAL(10, 2), nullable=False)
    booking_id = Column(Integer, ForeignKey("booking.booking_id"), nullable=False)
    package_type = Column(SQLEnum(PackageType, name="package_type_enum"), nullable=False)
    package_cost = Column(DECIMAL(10, 2), nullable=False)
    
    # Relationship back to Booking
    booking = relationship("Bookings", back_populates="booking_items")

    class Config:
        orm_mode = True