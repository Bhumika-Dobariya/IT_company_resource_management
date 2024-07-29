from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class CreateTimeTracking(BaseModel):
    emp_id : str
    date : datetime
    check_in_time : str
    check_out_time : str
    hours_worked : float
    status : str 
    extra_hours : float
    
    
class UpdateTimeTracking(BaseModel):
    emp_id : Optional[str] = None
    date : Optional[datetime] = None
    check_in_time : Optional[str] = None
    check_out_time : Optional[str] = None
    hours_worked : Optional[float] = None
    status : Optional[str] = None 
    extra_hours : Optional[float] = None
    
