from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ProjectCreate(BaseModel):
    manager_id: str
    emp_id: str
    Title: str
    Desciption: str
    start_date: str
    end_date: str
    status: str
    
    
class updateproject(BaseModel):
    manager_id: Optional[str] = None
    emp_id: Optional[str] = None
    Title: Optional[str] = None
    Desciption: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[str] = None
    
class CompletedProjectsCount(BaseModel):
    completed_projects_count: int