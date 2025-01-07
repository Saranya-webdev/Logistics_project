from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends

# Database URL
DATABASE_URL = 'mysql+pymysql://saranya:fullstackdeveloper%4016-17@localhost:3306/logisticsdb'

# Create engine and session local for database connection (Remove check_same_thread argument)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()  # Directly use the defined SessionLocal
    try:
        yield db
    finally:
        db.close()
