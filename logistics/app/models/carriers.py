from sqlalchemy import Integer, String, Column, DateTime,ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base
from sqlalchemy.orm import relationship



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
    account = relationship("CarrierAccount", uselist=False, back_populates="carrier")

    class Config:
        orm_mode = True

class CarrierAccount(Base):
    __tablename__ = 'carrier_account'
    __table_args__ = {'extend_existing': True}

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    carrier_id = Column(Integer, ForeignKey("carrier.carrier_id"), nullable=False)
    account_name = Column(String(255), nullable=False)
    account_number = Column(String(255), nullable=False)

    carrier = relationship("Carrier", back_populates="account")

    class Config:
        orm_mode = True





    
