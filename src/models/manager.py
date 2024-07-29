from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from datetime import datetime
from database.database import Base
import uuid

class Manager(Base):
    __tablename__ = 'managers'

    manager_id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    name = Column(String(50), index=True, nullable=False)
    role = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    phone_number = Column(String(10), nullable=True)
    department = Column(String(40), nullable=False)
    joining_date = Column(DateTime, default=datetime.now)
    address = Column(String(100), nullable=True)
    status = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)