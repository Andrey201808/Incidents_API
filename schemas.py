from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IncidentCreate(BaseModel):
    description: str
    source: str
    status: Optional[str] = "new"

class IncidentUpdate(BaseModel):
    status: str

class IncidentResponse(BaseModel):
    id: int
    description: str
    status: str
    source: str
    created_at: datetime

    class Config:
        from_attributes = True
