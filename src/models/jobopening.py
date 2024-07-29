from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from datetime import datetime
from database.database import Base
import uuid


class JobOpening(Base):
    
    __tablename__ = 'job_openings'

    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    department = Column(String(50), nullable=False)
    location = Column(String(100), nullable=False)
    experience_required = Column(String(100), nullable=True)
    education_required = Column(String(100), nullable=True)
    salary_range = Column(String(50), nullable=True)
    is_open = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)