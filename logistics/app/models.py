from sqlalchemy import Integer, String, Column, DateTime, ForeignKey,Enum,DECIMAL,Date,Time,Text
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship
import enum


# Customer Category Model
class CustomerCategory(Base):
    __tablename__ = 'customer_categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    customers = relationship("Customer", back_populates="category") #one to many customers for category

# Customer Type Model
class CustomerType(Base):
    __tablename__ = 'customer_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    customers = relationship("Customer", back_populates="customer_type")

# Customer Model
class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    mobile = Column(String(15))
    company = Column(String(255),nullable=False)
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
    category = relationship("CustomerCategory", back_populates="customers")
    customer_type = relationship("CustomerType", back_populates="customers")
    bookings = relationship('Bookings', back_populates='customer')

    class Config:
        orm_mode = True


class PickupMethod(str, enum.Enum):
    user_address = 'user_address'
    drop_point = 'drop_point'

class PackageType(str, enum.Enum):
    Box = 'Box'
    Envelope = 'Envelope' 
    Other = 'other'   

class PickupStatus(str,enum.Enum):
    pending = 'pending'
    confirmed = 'confirmed'
    shipped = 'shipped'
    delivered = 'delivered'
    cancelled = 'cancelled'

class Bookings(Base):
    __tablename__ = 'bookings'
    
    booking_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    created_by = Column(Integer, ForeignKey("users.user_id"))  # ForeignKey to the creator (User)
    pickup_method = Column(Enum(PickupMethod), nullable=False, name='pickup_method')
    booking_status = Column(Enum(PickupStatus), nullable=False, name='booking_status', default='pending')
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)

    name = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
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
    estimated_delivery_cost = Column(Integer, nullable=False)

    pickup_time = Column(Time, nullable=True)
    pickup_date = Column(Date, nullable=True)

    quotation_id = Column(Integer, ForeignKey('quotations.quotation_id'))

    # Define the relationships with the foreign key explicitly
    user = relationship("Users", back_populates="bookings", foreign_keys=[user_id])
    customer = relationship('Customer', back_populates='bookings')
    quotation = relationship('Quotations', back_populates='bookings', foreign_keys=[quotation_id])
    creator = relationship("Users", back_populates="created_bookings", foreign_keys=[created_by])
    booking_items = relationship("BookingItem", back_populates="booking")

class BookingItem(Base):
    __tablename__ = 'booking_items'

    item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"))
    weight = Column(DECIMAL(10, 2), nullable=False)
    length = Column(DECIMAL(10, 2), nullable=False)
    width = Column(DECIMAL(10, 2), nullable=False)
    height = Column(DECIMAL(10, 2), nullable=False)
    package_type = Column(Enum(PackageType), nullable=False, name='package_type')
    cost = Column(DECIMAL(10, 2), nullable=False)

    booking = relationship("Bookings", back_populates="booking_items")

class Quotations(Base):
    __tablename__ = "quotations"

    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    quotation_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    created_by = Column(Integer, ForeignKey("users.user_id"))
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"))

    pickup_method = Column(Enum(PickupMethod), nullable=False, name='pickup_method')
    booking_status = Column(Enum(PickupStatus), nullable=False, name='booking_status', default='pending')
    valid_until = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())

    user = relationship("Users", back_populates="quotations", foreign_keys=[user_id])  
    created_by_user = relationship("Users", back_populates="created_quotations", foreign_keys=[created_by])

    quotation_items = relationship("QuotationItems", back_populates="quotation")
    bookings = relationship('Bookings', back_populates='quotation', foreign_keys=[Bookings.quotation_id])

class QuotationItems(Base):
    __tablename__ = "quotation_items"

    item_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quotation_id = Column(Integer, ForeignKey("quotations.quotation_id"))
    weight = Column(DECIMAL(10, 2), nullable=False)
    length = Column(DECIMAL(10, 2), nullable=False)
    width = Column(DECIMAL(10, 2), nullable=False)
    height = Column(DECIMAL(10, 2), nullable=False)
    package_type = Column(Enum(PackageType), nullable=False, name='package_type')
    cost = Column(DECIMAL(10, 2), nullable=False)

    quotation = relationship("Quotations", back_populates="quotation_items")   

class AddressBook(Base):
    __tablename__ = "address_books"

    address_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))

    name = Column(String(255), nullable=False)
    address_line_1 = Column(String(255), nullable=False)
    address_line_2 = Column(String(255))
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    mobile = Column(String(15))
    created_at = Column(DateTime, nullable=False, default=func.now())

    user = relationship("Users", back_populates="address_books")     


# USERS
# Enum for roles
class UserRole(str, enum.Enum):
    logistic_company = 'logistic_company'
    agent = 'agent'
    employee = 'employee'
    customer = 'customer'

class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    mobile = Column(String(15))
    role = Column(Enum(UserRole), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    bookings = relationship("Bookings", back_populates="user", foreign_keys=[Bookings.user_id])
    quotations = relationship("Quotations", back_populates="user", foreign_keys=[Quotations.user_id])
    created_bookings = relationship("Bookings", back_populates="creator", foreign_keys=[Bookings.created_by])
    created_quotations = relationship("Quotations", back_populates="created_by_user", foreign_keys=[Quotations.created_by])
    address_books = relationship("AddressBook", back_populates="user")

    # user_permissions = relationship("UserPermission", back_populates="user")


# class UserPermission(Base):
#     __tablename__ = 'user_permissions'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), unique=True, nullable=False)
    
#     user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    
    # Define the reverse relationship with 'User'
    # user = relationship("User", back_populates="user_permissions")