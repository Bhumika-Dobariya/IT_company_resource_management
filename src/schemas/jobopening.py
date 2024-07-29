from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class JobOpeningBase(BaseModel):
    title: str
    description: str
    department: str
    location: str
    experience_required: str
    education_required: str
    salary_range: str
    is_open: bool
    
    
    
class UpdateJobopening(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    experience_required: Optional[str] = None
    education_required: Optional[str] = None
    salary_range: Optional[str] = None
    is_open: Optional[str] = None