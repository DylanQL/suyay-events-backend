from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, auth

router = APIRouter(prefix="/favorites", tags=["favorites"])

@router.get("/", response_model=List[schemas.FavoriteWithEvent])
def read_favorites(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Users can only see their own favorites
    if current_user.role.name != "Administrador" and user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud.get_favorites(db, user_id=user_id)

@router.post("/", response_model=schemas.Favorite)
def create_favorite(
    favorite: schemas.FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Users can only create favorites for themselves
    if current_user.role.name != "Administrador" and favorite.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only create favorites for yourself")
    
    # Check if favorite already exists
    existing_favorite = crud.get_favorite(db, user_id=favorite.user_id, event_id=favorite.event_id)
    if existing_favorite:
        raise HTTPException(status_code=400, detail="Event already in favorites")
    
    # Verify event exists
    db_event = crud.get_event(db, event_id=favorite.event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return crud.create_favorite(db=db, favorite=favorite)

@router.delete("/{favorite_id}")
def delete_favorite(
    favorite_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Find the favorite to check ownership
    all_favorites = crud.get_favorites(db, user_id=current_user.id)
    favorite = next((f for f in all_favorites if f.id == favorite_id), None)
    
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    # Users can only delete their own favorites
    if current_user.role.name != "Administrador" and favorite.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    crud.delete_favorite(db=db, favorite_id=favorite_id)
    return {"message": "Favorite removed successfully"}
