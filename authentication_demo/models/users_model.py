# Database table definitions
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True) # creates an index to speed up lookups.
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True, index=True)
    password = Column(String(300), nullable=False)
    is_active = Column(Boolean, default=True)