from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, auth

router = APIRouter(prefix="/purchases", tags=["purchases"])

@router.get("/", response_model=List[schemas.PurchaseWithDetails])
def read_purchases(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    event_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Regular users can only see their own purchases
    if current_user.role.name not in ["Administrador"] and user_id != current_user.id:
        user_id = current_user.id
    
    return crud.get_purchases(db, user_id=user_id, event_id=event_id, skip=skip, limit=limit)

@router.get("/{purchase_id}", response_model=schemas.PurchaseWithDetails)
def read_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_purchase = crud.get_purchase(db, purchase_id=purchase_id)
    if db_purchase is None:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    # Check if user can access this purchase
    if current_user.role.name != "Administrador" and db_purchase.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return db_purchase

@router.post("/", response_model=schemas.Purchase)
def create_purchase(
    purchase: schemas.PurchaseCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Users can only create purchases for themselves
    if current_user.role.name != "Administrador" and purchase.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only create purchases for yourself")
    
    # Verify event exists
    db_event = crud.get_event(db, event_id=purchase.event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return crud.create_purchase(db=db, purchase=purchase)
