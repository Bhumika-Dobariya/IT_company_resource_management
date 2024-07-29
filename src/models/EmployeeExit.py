
from sqlalchemy import Column, Integer,Date,Text,DateTime,String,ForeignKey
from database.database import Base
from datetime import datetime
import uuid


class EmployeeExit(Base):
    
    __tablename__ = "employee_exit"
    
    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    employee_id = Column(String(50), ForeignKey('employees.id'), nullable=False)
    exit_date = Column(Date, nullable=False)
    reason_for_exit = Column(String(200))
    created_at = Column(DateTime, default=datetime.now)