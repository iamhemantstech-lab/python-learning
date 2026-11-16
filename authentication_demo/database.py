# MySQL connection
from sqlalchemy import create_engine 
#creates the connection interface between SQLAlchemy and MySQL.
from sqlalchemy.orm import sessionmaker, declarative_base
# sessionmaker: creates database sessions for performing queries.
# declarative_base: provides a base class for defining database models.

from config import settings

DATABASE_URL = settings.DATABASE_URL

# create database engine
engine = create_engine(DATABASE_URL)

# create database session
LocalSession = sessionmaker(
    autoflush=False, #Changes are not automatically flushed before queries
    autocommit=False, #Changes are not automatically committed
    bind=engine #Connects sessions to our MySQL engine
)

# Base class for database models
Base = declarative_base()

def get_db():
    db = LocalSession()
    try:
        yield db # yield pauses the function and allows it to continue later.

    finally:
        db.close()