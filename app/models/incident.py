from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class IncidentStatus(str, enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class IncidentSource(str, enum.Enum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"
    OTHER = "other"

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(SAEnum(IncidentStatus), default=IncidentStatus.NEW, nullable=False)
    source = Column(SAEnum(IncidentSource), default=IncidentSource.OTHER, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
