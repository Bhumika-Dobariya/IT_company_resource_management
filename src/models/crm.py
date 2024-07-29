from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from database.database import Base
import uuid

class Customer(Base):
    #customer relationship management
    
    __tablename__ = 'crm_customers'

    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)
    industry = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)