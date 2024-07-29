from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class createattendence(BaseModel):
    
    employee_id : str
    check_in_time : datetime
    check_out_time : datetime
    is_present :bool
    
    
class updateattendence(BaseModel):
    
    employee_id : Optional[str] = None
    check_in_time : Optional[datetime] = None
    check_out_time : Optional[datetime] = None
    is_present :Optional[bool] = None