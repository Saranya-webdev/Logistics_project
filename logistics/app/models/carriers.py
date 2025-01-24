from sqlalchemy import Integer, String, Column, DateTime,Boolean
from sqlalchemy.sql import func
from app.models.base import Base


# carrier Model
class Carrier(Base):
    __tablename__ = 'carrier'
    __table_args__ = {'extend_existing': True}

    carrier_id = Column(Integer, primary_key=True, autoincrement=True)
    carrier_name = Column(String(255), nullable=False)
    carrier_mobile = Column(String(15))
    carrier_email = Column(String(255), nullable=False, unique=True)
    carrier_address = Column(String(255), nullable=False)
    carrier_city = Column(String(255), nullable=False)
    carrier_state = Column(String(255), nullable=False)
    carrier_country = Column(String(255), nullable=False)
    carrier_pincode = Column(String(255), nullable=True)
    carrier_geolocation = Column(String(255), nullable=False)
    
    remarks = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    active_flag = Column(Integer, default=1)
    deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    # created_by = Column(Integer, ForeignKey("user.user_id"))
    # updated_by = Column(Integer, ForeignKey("user.user_id"))

    is_active = Column(Boolean, default=True, comment="Indicates if the carrier is active) or not")

    class Config:
        orm_mode = True



    
