from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from datetime import datetime
from database.database import Base
import uuid


class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    employee_id = Column(String(50), ForeignKey('employees.id'), nullable=False)
    check_in_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    check_out_time = Column(DateTime)
    is_present = Column(Boolean, default=True)