from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ManagerAll(BaseModel):
    name: str
    role:str
    email: str
    phone_number: str
    department: str
    joining_date: datetime
    address:str
    status: str
    
    
class UpdateManager(BaseModel):
    name: Optional[str] = None
    role : Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    department: Optional[str] = None
    joining_date: Optional[datetime] = None
    address:Optional[str] = None
    status: Optional[str] = None
    