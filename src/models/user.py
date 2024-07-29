
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from database.database import Base
import uuid

class User(Base):
    
    __tablename__ = "users"

    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(200), default="user")  
    last_login = Column(DateTime)
    phone_number = Column(String(10), nullable=True)
    created_at = Column(DateTime,default=datetime.now)
    modified_at = Column(DateTime,default=datetime.now,onupdate=datetime.now)
    is_active = Column(Boolean, default= True)
    is_deleted = Column(Boolean, default= False)
    is_verified = Column(Boolean, default=False)
   
