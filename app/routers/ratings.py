from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, auth

router = APIRouter(prefix="/ratings", tags=["ratings"])

@router.get("/", response_model=List[schemas.RatingWithDetails])
def read_ratings(
    event_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_ratings(db, event_id=event_id, user_id=user_id)

@router.post("/", response_model=schemas.Rating)
def create_rating(
    rating: schemas.RatingCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Users can only create ratings for themselves
    if current_user.role.name != "Administrador" and rating.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only create ratings for yourself")
    
    # Check if rating already exists
    existing_rating = crud.get_rating(db, user_id=rating.user_id, event_id=rating.event_id)
    if existing_rating:
        raise HTTPException(status_code=400, detail="Rating already exists for this event")
    
    # Verify event exists
    db_event = crud.get_event(db, event_id=rating.event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return crud.create_rating(db=db, rating=rating)
