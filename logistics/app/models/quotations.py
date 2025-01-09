from sqlalchemy import Integer,Column, DateTime, ForeignKey,Enum,DECIMAL,Date
from sqlalchemy.sql import func
from app.models.base import Base
from sqlalchemy.orm import relationship
from app.models.bookings import Bookings, PickupMethod, PickupStatus,PackageType

# Quotation Model
class Quotations(Base):
    __tablename__ = "quotations"

    quotation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    created_by = Column(Integer, ForeignKey("users.user_id"))
    pickup_method = Column(Enum(PickupMethod), nullable=False, name='pickup_method')
    booking_status = Column(Enum(PickupStatus), nullable=False, name='booking_status', default='pending')
    valid_until = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"))
    user = relationship("Users", back_populates="quotations", foreign_keys=[user_id])  
    created_by_user = relationship("Users", back_populates="created_quotations", foreign_keys=[created_by])
    quotation_items = relationship("QuotationItems", back_populates="quotation")
    bookings = relationship('Bookings', back_populates='quotation', foreign_keys=[Bookings.quotation_id])

# Quotation Item Model
class QuotationItems(Base):
    __tablename__ = "quotation_items"

    item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quotation_id = Column(Integer, ForeignKey("quotations.quotation_id"), nullable=False)
    weight = Column(DECIMAL(10, 2), nullable=False)
    length = Column(DECIMAL(10, 2), nullable=False)
    width = Column(DECIMAL(10, 2), nullable=False)
    height = Column(DECIMAL(10, 2), nullable=False)
    package_type = Column(Enum(PackageType), nullable=False, name='package_type')
    cost = Column(DECIMAL(10, 2), nullable=False)
    quotation = relationship("Quotations", back_populates="quotation_items")   
