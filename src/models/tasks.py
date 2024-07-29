
from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from datetime import datetime
from database.database import Base
import uuid


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(String(50), primary_key=True, default=str(uuid.uuid4()))
    emp_id = Column(String(50), ForeignKey('employees.id'), nullable=False)
    project_id = Column(String(50), ForeignKey('project.id'), nullable=False)
    title = Column(String(100), index=True, nullable=False)
    description = Column(String(300), nullable=True)
    status = Column(String(50), nullable=False, default="todo")
    created_at = Column(DateTime, default=datetime.now)
    due_date = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)