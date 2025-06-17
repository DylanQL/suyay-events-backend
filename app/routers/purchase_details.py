from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, auth

router = APIRouter(prefix="/purchase-details", tags=["purchase-details"])

@router.get("/", response_model=List[schemas.PurchaseDetail])
def read_purchase_details(
    purchase_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Verify purchase exists and user has access
    db_purchase = crud.get_purchase(db, purchase_id=purchase_id)
    if not db_purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    if current_user.role.name != "Administrador" and db_purchase.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud.get_purchase_details(db, purchase_id=purchase_id)

@router.post("/", response_model=schemas.PurchaseDetail)
def create_purchase_detail(
    purchase_detail: schemas.PurchaseDetailCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Verify purchase exists and user has access
    db_purchase = crud.get_purchase(db, purchase_id=purchase_detail.purchase_id)
    if not db_purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    if current_user.role.name != "Administrador" and db_purchase.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud.create_purchase_detail(db=db, purchase_detail=purchase_detail)
