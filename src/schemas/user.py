from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class userschema(BaseModel):
    username :str
    email : str
    password : str
    role : str  
    last_login :datetime
    phone_number : str
    
class updateuser(BaseExceptionGroup):
    username :Optional[str] = None
    email : Optional[str] = None
    password : Optional[str] = None
    role : Optional[str] = None  
    last_login : Optional[str] = None
    phone_number : Optional[str] = None
    