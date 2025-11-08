from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import SessionLocal, get_db
from models import Incident, IncidentStatus
from schemas import IncidentCreate, IncidentUpdate, IncidentResponse

app = FastAPI(title="Incident Tracker API")

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/incidents/", response_model=IncidentResponse, status_code=201)
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db_session)):
    # Проверим, что статус допустим
    valid_statuses = [IncidentStatus.NEW, IncidentStatus.IN_PROGRESS, 
                      IncidentStatus.RESOLVED, IncidentStatus.CLOSED, IncidentStatus.PENDING]
    if incident.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    db_incident = Incident(
        description=incident.description,
        source=incident.source,
        status=incident.status
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@app.get("/incidents/", response_model=List[IncidentResponse])
def get_incidents(
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db_session)
):
    query = db.query(Incident)
    if status:
        query = query.filter(Incident.status == status)
    
    incidents = query.all()
    return incidents

@app.put("/incidents/{incident_id}/status", response_model=IncidentResponse)
def update_incident_status(
    incident_id: int, 
    incident_update: IncidentUpdate, 
    db: Session = Depends(get_db_session)
):
    # Проверим, что статус допустим
    valid_statuses = [IncidentStatus.NEW, IncidentStatus.IN_PROGRESS, 
                      IncidentStatus.RESOLVED, IncidentStatus.CLOSED, IncidentStatus.PENDING]
    if incident_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    db_incident.status = incident_update.status
    db.commit()
    db.refresh(db_incident)
    return db_incident

# Создание таблиц при запуске
@app.on_event("startup")
def startup_event():
    from database import Base, engine
    Base.metadata.create_all(bind=engine)
