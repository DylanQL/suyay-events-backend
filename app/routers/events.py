from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, auth

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/", response_model=List[schemas.EventWithDetails])
def read_events(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    organizer_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_events(db, skip=skip, limit=limit, category_id=category_id, organizer_id=organizer_id)

@router.get("/{event_id}", response_model=schemas.EventWithDetails)
def read_event(
    event_id: int,
    db: Session = Depends(get_db)
):
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.post("/", response_model=schemas.Event)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_organizer_user)
):
    # Ensure the organizer is creating events for themselves
    organizer = crud.get_organizer_by_user(db, user_id=current_user.id)
    if not organizer:
        raise HTTPException(status_code=400, detail="User is not an organizer")
    
    if organizer.id != event.organizer_id:
        raise HTTPException(status_code=403, detail="Can only create events for your own organization")
    
    return crud.create_event(db=db, event=event)

@router.patch("/{event_id}", response_model=schemas.Event)
def update_event(
    event_id: int,
    event_update: schemas.EventUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Only admin or the event organizer can update
    if current_user.role.name != "Administrador" and db_event.organizer_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud.update_event(db=db, event_id=event_id, event_update=event_update)

@router.delete("/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Only admin or the event organizer can delete
    if current_user.role.name != "Administrador" and db_event.organizer_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    crud.delete_event(db=db, event_id=event_id)
    return {"message": "Event deleted successfully"}
