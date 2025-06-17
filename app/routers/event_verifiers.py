from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, auth

router = APIRouter(prefix="/event-verifiers", tags=["event-verifiers"])

@router.get("/", response_model=List[schemas.EventVerifier])
def read_event_verifiers(
    event_id: Optional[int] = None,
    verifier_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    return crud.get_event_verifiers(db, event_id=event_id, verifier_id=verifier_id)

@router.post("/", response_model=schemas.EventVerifier)
def create_event_verifier(
    event_verifier: schemas.EventVerifierCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Check if event exists and user has permission
    db_event = crud.get_event(db, event_id=event_verifier.event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Only admin or event organizer can assign verifiers
    if current_user.role.name != "Administrador" and db_event.organizer_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud.create_event_verifier(db=db, event_verifier=event_verifier)

@router.delete("/{event_verifier_id}")
def delete_event_verifier(
    event_verifier_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_event_verifier = crud.get_event_verifiers(db)
    event_verifier = next((ev for ev in db_event_verifier if ev.id == event_verifier_id), None)
    
    if not event_verifier:
        raise HTTPException(status_code=404, detail="Event verifier not found")
    
    # Check permissions through the event
    db_event = crud.get_event(db, event_id=event_verifier.event_id)
    if current_user.role.name != "Administrador" and db_event.organizer_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    crud.delete_event_verifier(db=db, event_verifier_id=event_verifier_id)
    return {"message": "Event verifier removed successfully"}
