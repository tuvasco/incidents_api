from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class IncidentStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

class IncidentSource(str, Enum):
    operator = "operator"
    monitoring = "monitoring"
    partner = "partner"
    other = "other"

class IncidentCreate(BaseModel):
    description: str = Field(..., min_length=3, max_length=2000)
    source: Optional[IncidentSource] = IncidentSource.other

class IncidentUpdateStatus(BaseModel):
    status: IncidentStatus

class IncidentRead(BaseModel):
    id: int
    description: str
    status: IncidentStatus
    source: IncidentSource
    created_at: datetime

    class Config:
        orm_mode = True
