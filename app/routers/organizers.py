from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, auth

router = APIRouter(prefix="/organizers", tags=["organizers"])

@router.get("/", response_model=List[schemas.OrganizerWithUser])
def read_organizers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    return crud.get_organizers(db, skip=skip, limit=limit)

@router.get("/{organizer_id}", response_model=schemas.OrganizerWithUser)
def read_organizer(
    organizer_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_organizer = crud.get_organizer(db, organizer_id=organizer_id)
    if db_organizer is None:
        raise HTTPException(status_code=404, detail="Organizer not found")
    return db_organizer

@router.post("/", response_model=schemas.Organizer)
def create_organizer(
    organizer: schemas.OrganizerCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Check if user already has an organizer profile
    existing_organizer = crud.get_organizer_by_user(db, user_id=organizer.user_id)
    if existing_organizer:
        raise HTTPException(status_code=400, detail="User already has an organizer profile")
    
    return crud.create_organizer(db=db, organizer=organizer)

@router.patch("/{organizer_id}", response_model=schemas.Organizer)
def update_organizer(
    organizer_id: int,
    organizer_update: schemas.OrganizerUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_organizer = crud.get_organizer(db, organizer_id=organizer_id)
    if db_organizer is None:
        raise HTTPException(status_code=404, detail="Organizer not found")
    
    # Only admin or the organizer themselves can update
    if current_user.role.name != "Administrador" and db_organizer.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud.update_organizer(db=db, organizer_id=organizer_id, organizer_update=organizer_update)
