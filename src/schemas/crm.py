from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CustomerBase(BaseModel):
    
    name :str
    email : str
    phone_number : str
    address : str
    industry : str
    
    
class updatecustomer(BaseModel):
    
    name :Optional[str] = None
    email : Optional[str] = None
    phone_number : Optional[str] = None
    address : Optional[str] = None
    industry : Optional[str] = None