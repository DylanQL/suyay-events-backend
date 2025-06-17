from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, auth

router = APIRouter(prefix="/claims", tags=["claims"])

@router.get("/", response_model=List[schemas.ClaimWithDistrict])
def read_claims(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_admin_user)
):
    return crud.get_claims(db, skip=skip, limit=limit)

@router.get("/{claim_id}", response_model=schemas.ClaimWithDistrict)
def read_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_admin_user)
):
    db_claim = crud.get_claim(db, claim_id=claim_id)
    if db_claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")
    return db_claim

@router.post("/", response_model=schemas.Claim)
def create_claim(
    claim: schemas.ClaimCreate,
    db: Session = Depends(get_db)
):
    return crud.create_claim(db=db, claim=claim)

@router.patch("/{claim_id}", response_model=schemas.Claim)
def update_claim(
    claim_id: int,
    claim_update: schemas.ClaimUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_admin_user)
):
    db_claim = crud.get_claim(db, claim_id=claim_id)
    if db_claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")
    
    return crud.update_claim(db=db, claim_id=claim_id, claim_update=claim_update)
