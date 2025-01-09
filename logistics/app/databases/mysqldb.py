# Environment Variables: Used load_dotenv to load environment variables from a .env file for better security. The database URL is now fetched from the environment variable.

# Comments: Added more descriptive comments to improve clarity.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://saranya:fullstackdeveloper%4016-17@localhost:3306/logisticsdb')

# Create engine and session local for database connection
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
