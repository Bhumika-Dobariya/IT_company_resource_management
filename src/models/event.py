
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from database.database import Base
import uuid



class Event(Base):
    __tablename__ = 'events'

    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    start_time = Column(String(20), nullable=False)
    end_time = Column(String(20), nullable=False)
    location = Column(String(200), nullable=True)
    organizer = Column(String(100), nullable=True)
    type = Column(String(50), nullable=False)  
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)