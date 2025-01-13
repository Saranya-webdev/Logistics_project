from sqlalchemy import Integer, String, Column, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base
from sqlalchemy.orm import relationship

# Address Book Model
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
    