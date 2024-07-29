from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from datetime import datetime
from database.database import Base
import uuid

class Projects(Base):
    
    __tablename__ = "project"

    id = Column(String(50), primary_key=True, default=str(uuid.uuid4())) 
    manager_id = Column(String(50), ForeignKey('managers.manager_id'), nullable=False)
    emp_id = Column(String(50), ForeignKey('employees.id'), nullable=False)
    Title = Column(String(50), index=True, nullable=False)
    Desciption = Column(String(300), index=True, nullable=False)
    start_date = Column(String(50), nullable=True)
    end_date = Column(String(50), nullable=True)
    status = Column(String(30), index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    