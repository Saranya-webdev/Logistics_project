from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from fastapi import Depends

# Database URL
URL_DATABASE = 'mysql+pymysql://saranya:fullstackdeveloper%4016-17@localhost:3306/logisticsdb'

# Create engine and session local for database connection
engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Database session dependency
def get_db():
    db = SessionLocal() #returns new database session connected to the database engine.
    try:
        yield db #return the session
    finally:
        db.close() #database session is closed after the request is complete,releasing the connection