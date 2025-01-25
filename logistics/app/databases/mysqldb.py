import os
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Fetch the database URL from the environment, with a fallback if not found
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://saranya:fullstackdeveloper%4016-17@localhost:3306/logisticsdb')

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create engine and session local for database connection
try:
    engine: Engine = create_engine(DATABASE_URL)
    logger.info("Database engine created successfully.")
except Exception as e:
    logger.error(f"Error creating database engine: {e}")
    raise

# SessionLocal for session management, which is later used to get database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()

# Dependency to get the DB session
def get_db() -> Session:
    db: Session = SessionLocal()  # Create a new database session
    try:
        yield db  # Yield the session for usage
    finally:
        db.close()  # Ensure the session is closed after usage