
from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey,Float
from datetime import datetime
from database.database import Base
import uuid


class TimeTracking(Base):
    
    __tablename__ = 'time_tracking'

    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    emp_id = Column(String(50), ForeignKey('employees.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    check_in_time = Column(String(20), nullable=False)
    check_out_time = Column(String(20), nullable=True)
    hours_worked = Column(Float, nullable=True)
    status = Column(String(20), nullable=True) 
    extra_hours = Column(Float, nullable=True)

