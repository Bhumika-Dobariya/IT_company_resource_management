from pydantic import BaseModel
from datetime import date
from typing import Optional

class NEmployeeExit(BaseModel):
    employee_id: str
    exit_date: date
    reason_for_exit: Optional[str]