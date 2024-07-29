from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EmployeeBase(BaseModel):
    manager_id:str
    name: str
    email: str
    position: str
    role: str
    department: str
    DOB: str
    salary: int
    address: str
    phone_number: str
    
    
class EmployeeUpdate(EmployeeBase):
    manager_id : Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    position: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    DOB: Optional[str] = None
    salary: Optional[int] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None