from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.services.incident_service import IncidentService
from app.schemas.incident import IncidentCreate, IncidentRead, IncidentUpdateStatus, IncidentStatus as StatusEnum

router = APIRouter(prefix="/incidents", tags=["incidents"])

@router.post("/", response_model=IncidentRead, status_code=status.HTTP_201_CREATED)
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    service = IncidentService(db)
    incident = service.create_incident(payload)
    return incident

@router.get("/", response_model=List[IncidentRead])
def list_incidents(status: Optional[StatusEnum] = Query(None), db: Session = Depends(get_db)):
    service = IncidentService(db)
    incidents = service.list_incidents(status)
    return incidents

@router.patch("/{incident_id}", response_model=IncidentRead)
def update_incident_status(incident_id: int, payload: IncidentUpdateStatus, db: Session = Depends(get_db)):
    service = IncidentService(db)
    updated = service.update_status(incident_id, payload.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Incident not found")
    return updated
