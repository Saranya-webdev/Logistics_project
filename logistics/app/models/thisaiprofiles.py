from sqlalchemy import Integer, String, Column, DateTime, Boolean, ForeignKey,Enum
from sqlalchemy.sql import func
from app.models.base import Base
from app.models.enums import VerificationStatus, Role
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum 

# associates Model
class Associate(Base):
    __tablename__ = 'thisai_associates'
    __table_args__ = {'extend_existing': True}

    associates_id = Column(Integer, primary_key=True, autoincrement=True)
    associates_name = Column(String(255), nullable=False)
    associates_mobile = Column(String(15))
    associates_email = Column(String(255), nullable=False, unique=True)
    associates_role = Column(SQLAlchemyEnum(Role), nullable=False)
    associates_verification_status = Column(
    Enum(VerificationStatus, native_enum=False),
    nullable=False,
    default=VerificationStatus.NoneValue.value)
    remarks = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    active_flag = Column(Integer, default=1)

    associates_credentials = relationship(
        "AssociatesCredential",
        back_populates="associate",
        cascade="all, delete-orphan"
    )

    class Config:
        orm_mode = True


class AssociatesCredential(Base):
    __tablename__ = 'associates_credential'
    __table_args__ = {'extend_existing': True}

    associates_credential_id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    associates_id = Column(Integer, ForeignKey("thisai_associates.associates_id", ondelete="CASCADE"))
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    associate = relationship("Associate", back_populates="associates_credentials")  


    class Config:
        orm_mode = True
