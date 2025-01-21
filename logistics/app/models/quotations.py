from sqlalchemy import Integer, Column, DateTime, ForeignKey, Enum, DECIMAL, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.enums import PickupMethod, PickupStatus, PackageType
from app.models.bookings import Bookings


class Quotations(Base):
    __tablename__ = "quotation"
    __table_args__ = {'extend_existing': True}

    quotation_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))  # Correct reference
    created_by = Column(Integer, ForeignKey("customer.customer_id"))  # Correct reference
    pickup_method = Column(Enum(PickupMethod), nullable=False, name='pickup_method')
    status = Column(Enum(PickupStatus), default='active', nullable=False, name='status')
    valid_until = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    quotation_status = Column(Enum(PickupStatus), nullable=True)

    # Correct relationships with foreign_keys argument
    quotation_items = relationship("QuotationItems", back_populates="quotation", cascade="all, delete-orphan")
    bookings = relationship('Bookings', back_populates='quotation', foreign_keys=[Bookings.quotation_id])  # Specify foreign key

    customer = relationship('Customer', back_populates='quotations', foreign_keys=[customer_id])

    class Config:
        orm_mode = True






class QuotationItems(Base):
    __tablename__ = "quotation_items"
    __table_args__ = {'extend_existing': True}

    item_id = Column(Integer, primary_key=True,  autoincrement=True)
    quotation_id = Column(Integer, ForeignKey("quotation.quotation_id"), nullable=False)  # Correct reference
    weight = Column(DECIMAL(10, 2), nullable=False)
    length = Column(DECIMAL(10, 2), nullable=False)
    width = Column(DECIMAL(10, 2), nullable=False)
    height = Column(DECIMAL(10, 2), nullable=False)
    package_type = Column(Enum(PackageType), nullable=False, name='package_type')
    cost = Column(DECIMAL(10, 2), nullable=False)

    # Relationship back to Quotations
    quotation = relationship("Quotations", back_populates="quotation_items")

    class Config:
        orm_mode = True
