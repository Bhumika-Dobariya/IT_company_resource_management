from datetime import datetime
from pydantic import BaseModel
from typing import Optional



class TaskCreate(BaseModel):
    emp_id : str
    project_id:str
    title : str
    description : str
    status : str
    due_date : str
    

class TaskUpdate(BaseModel):
    emp_id : Optional[str] = None
    project_id:Optional[str] = None
    title : Optional[str] = None
    description : Optional[str] = None
    status : Optional[str] = None
    due_date : Optional[str] = None