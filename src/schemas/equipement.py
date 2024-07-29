from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class EquipmentBase(BaseModel):
    name: str
    type: str
    purchase_date: datetime
    status: str
    assigned_to:str
    value: float
    
class UpdateEquipment(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    purchase_date: Optional[datetime] = None
    status: Optional[str] = None
    assigned_to:Optional[str] = None
    value: Optional[float] = None