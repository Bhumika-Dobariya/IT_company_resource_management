
from datetime import datetime
from pydantic import BaseModel
from typing import Optional



class CreateEvent(BaseModel):
    name: str
    description: str
    start_time: str
    end_time: str
    location: str
    organizer: str
    type: str
    
    
class UpdateEvent(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    organizer: Optional[str] = None
    type: Optional[str] = None