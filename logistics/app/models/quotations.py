from sqlalchemy import Integer, Column,ForeignKey, Enum, DECIMAL, Date,Enum as SQLEnum,String,Date
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.enums import QuotationStatus, PackageType

class Quotations(Base):
    __tablename__ = 'quotation'
    __table_args__ = {'extend_existing': True}

    quotation_id = Column(Integer, primary_key=True, autoincrement=True)
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
    booking_by = Column(Integer, ForeignKey("customer.customer_id"))
    total_cost = Column(DECIMAL(10, 2), nullable=False)
    status = Column(SQLEnum(QuotationStatus, name="quotation_status_enum"), default=QuotationStatus.unsaved,nullable=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))

    # Relationships
    customer = relationship("Customer", back_populates="quotations", foreign_keys=[customer_id])
    quotation_items = relationship("QuotationItems", back_populates="quotation")
    
    class Config:
        orm_mode = True


class QuotationItems(Base):
    __tablename__ = "quotation_items"
    __table_args__ = {'extend_existing': True}

    item_id = Column(Integer, primary_key=True, autoincrement=True)
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
