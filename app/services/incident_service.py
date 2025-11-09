from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import IncidentCreate
from app.models.incident import Incident, IncidentStatus

class IncidentService:
    def __init__(self, db: Session):
        self.repo = IncidentRepository(db)

    def create_incident(self, payload: IncidentCreate) -> Incident:
        return self.repo.create(payload)

    def get_incident(self, incident_id: int) -> Optional[Incident]:
        return self.repo.get_by_id(incident_id)

    def list_incidents(self, status: Optional[IncidentStatus] = None) -> List[Incident]:
        return self.repo.list(status)

    def update_status(self, incident_id: int, status: IncidentStatus) -> Optional[Incident]:
        incident = self.repo.get_by_id(incident_id)
        if not incident:
            return None
        return self.repo.update_status(incident, status)
