from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Boolean, DECIMAL, Enum
from sqlalchemy.sql import func
from app.models.base import Base
from sqlalchemy.orm import relationship
from app.models.bookings import Bookings
from app.models.quotations import Quotations
from app.models.enums import Type,Category


# Enum definitions for CustomerType and CustomerCategory

# Your Customer model
class Customer(Base):
    __tablename__ = 'customer'
    __table_args__ = {'extend_existing': True}

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(255), nullable=False)
    customer_mobile = Column(String(15))
    customer_email = Column(String(255), nullable=False, unique=True)
    customer_address = Column(String(255), nullable=False)
    customer_city = Column(String(255), nullable=False)
    customer_state = Column(String(255), nullable=False)
    customer_country = Column(String(255), nullable=False)
    customer_pincode = Column(String(255), nullable=True)
    customer_geolocation = Column(String(255), nullable=False)

    customer_type = Column(
        Enum(Type, name="customer_type_enum"), nullable=False
    )

    customer_category = Column(
        Enum(Category, name="customer_category_enum"), nullable=False
    )

    remarks = Column(String(255), nullable=True)
    verification_status = Column(String(255), nullable=False, default="none")
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    active_flag = Column(Integer, default=1)
    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    bookings = relationship('Bookings', back_populates='customer', foreign_keys=[Bookings.customer_id], cascade="all, delete-orphan")
    address_books = relationship("AddressBook", back_populates="customer", cascade="all, delete-orphan")
    quotations = relationship("Quotations", back_populates="customer", foreign_keys=[Quotations.customer_id], cascade="all, delete-orphan")

    # Added relationship to customer_business
    customer_business = relationship("CustomerBusiness", back_populates="customer", uselist=False, cascade="all, delete-orphan")
    # Added relationship to customer_credential
    customer_credentials = relationship("CustomerCredential", back_populates="customer", uselist=False, cascade="all, delete-orphan")
    # Added relationship to customer_margin
    customer_margins = relationship("CustomerMargin", back_populates="customer", uselist=False, cascade="all, delete-orphan")
    # Added relationship to customer_payments
    customer_payments = relationship("CustomerPayments", back_populates="customer", cascade="all, delete-orphan")

    class Config:
        orm_mode = True


class CustomerBusiness(Base):
    __tablename__ = 'customer_business' 
    __table_args__ = {'extend_existing': True} 

    business_id = Column(Integer, primary_key=True)
    tax_id = Column(String(255), nullable=False)
    license_number = Column(String(255), nullable=False)
    designation = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, comment="Indicates if the customer is active or not")

    customer = relationship("Customer", back_populates="customer_business")

    class Config:
        orm_mode = True


    
class CustomerCredential(Base):
    __tablename__ = 'customer_credential'
    __table_args__ = {'extend_existing': True}

    customer_credential_id = Column(Integer, primary_key=True)
    email_id = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))  # Added customer_id field
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, comment="Indicates if the customer is active or not")

    customer = relationship("Customer", back_populates="customer_credentials")

    class Config:
        orm_mode = True

class CustomerMargin(Base):
    __tablename__ = 'customer_margin'
    __table_args__ = {'extend_existing': True}

    customer_margin_id = Column(Integer, primary_key=True)
    customer_type = Column(Enum(Type, name="customer_type_enum"), nullable=True)
    cost = Column(DECIMAL(10, 2), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))  # Added customer_id field
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, comment="Indicates if the customer is active or not")

    customer = relationship("Customer", back_populates="customer_margins")

    class Config:
        orm_mode = True

    
class CustomerPayments(Base):
    __tablename__ = 'customer_payment'
    __table_args__ = {'extend_existing': True}

    customer_payment_id = Column(Integer, primary_key=True)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_mode = Column(String(255), nullable=False)
    booking_id = Column(Integer, ForeignKey("booking.booking_id"), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))  # Added customer_id field
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True, comment="Indicates if the customer is active or not")

    customer = relationship("Customer", back_populates="customer_payments")
    booking = relationship("Bookings", back_populates="customer_payments")

    class Config:
        orm_mode = True