# Database table definitions
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True) # creates an index to speed up lookups.
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True, index=True)
    password = Column(String(300), nullable=False)
    mobile_number = Column(String(20), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
