from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.incident import Incident, IncidentStatus, IncidentSource
from app.schemas.incident import IncidentCreate

class IncidentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: IncidentCreate) -> Incident:
        incident = Incident(
            description=payload.description,
            source=IncidentSource(payload.source.value) if hasattr(payload, "source") else IncidentSource.other,
            status=IncidentStatus.NEW,
        )
        self.db.add(incident)
        self.db.commit()
        self.db.refresh(incident)
        return incident

    def get_by_id(self, incident_id: int) -> Optional[Incident]:
        return self.db.query(Incident).filter(Incident.id == incident_id).first()

    def list(self, status: Optional[IncidentStatus] = None) -> List[Incident]:
        q = self.db.query(Incident)
        if status:
            q = q.filter(Incident.status == status)
        return q.order_by(Incident.created_at.desc()).all()

    def update_status(self, incident: Incident, new_status: IncidentStatus) -> Incident:
        incident.status = new_status
        self.db.add(incident)
        self.db.commit()
        self.db.refresh(incident)
        return incident
