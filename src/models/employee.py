from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from datetime import datetime
from database.database import Base
import uuid

class Employee(Base):
    __tablename__ = "employees"

    id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    manager_id = Column(String(50), ForeignKey('managers.manager_id'), nullable=False)
    name = Column(String(50), nullable=False)
    department = Column(String(40), nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    position = Column(String(30), nullable=False)
    role = Column(String(50), nullable=False)
    address = Column(String(100), nullable=True)
    DOB = Column(String(15), nullable=False)
    date_hired = Column(DateTime, default=datetime.now)
    phone_number = Column(String(15), unique=True, nullable=False)
    salary = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)