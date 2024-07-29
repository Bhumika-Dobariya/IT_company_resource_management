from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey,Float
from datetime import datetime
from database.database import Base
import uuid

class Equipment(Base):
    
    __tablename__ = 'equipment'

    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    type = Column(String(100), nullable=False)
    purchase_date = Column(DateTime, default=datetime.now, nullable=False)
    status = Column(String(50), nullable=False)
    assigned_to = Column(String(50), ForeignKey('employees.id'), nullable=True)
    value = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)