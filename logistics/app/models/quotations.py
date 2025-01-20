from sqlalchemy import Integer, Column, DateTime, ForeignKey, Enum, DECIMAL, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.enums import PickupMethod, PickupStatus, PackageType
from app.models.bookings import Bookings


class Quotations(Base):
    __tablename__ = "quotations"

    quotation_id = Column(Integer, primary_key=True,autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    created_by = Column(Integer, ForeignKey("customers.customer_id"))
    pickup_method = Column(Enum(PickupMethod), nullable=False, name='pickup_method')
    status = Column(Enum(PickupStatus), default='active', nullable=False, name='status')
    valid_until = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    quotation_status = Column(Enum(PickupStatus), nullable=True)

    # Relationships
    quotation_items = relationship("QuotationItems", back_populates="quotation", uselist=True)
    bookings = relationship('Bookings', back_populates='quotation', foreign_keys=[Bookings.quotation_id])

    # Specify which foreign key to use in the relationship
    customer = relationship('Customer', back_populates='quotations', foreign_keys=[customer_id])



class QuotationItems(Base):
    __tablename__ = "quotation_items"

    item_id = Column(Integer, primary_key=True,  autoincrement=True)
    quotation_id = Column(Integer, ForeignKey("quotations.quotation_id"), nullable=False)
    weight = Column(DECIMAL(10, 2), nullable=False)
    length = Column(DECIMAL(10, 2), nullable=False)
    width = Column(DECIMAL(10, 2), nullable=False)
    height = Column(DECIMAL(10, 2), nullable=False)
    package_type = Column(Enum(PackageType), nullable=False, name='package_type')
    cost = Column(DECIMAL(10, 2), nullable=False)

    quotation = relationship("Quotations", back_populates="quotation_items")
