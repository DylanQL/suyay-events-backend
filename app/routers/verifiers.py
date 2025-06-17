from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, auth

router = APIRouter(prefix="/verifiers", tags=["verifiers"])

@router.get("/", response_model=List[schemas.VerifierWithDetails])
def read_verifiers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    return crud.get_verifiers(db, skip=skip, limit=limit)

@router.get("/{verifier_id}", response_model=schemas.VerifierWithDetails)
def read_verifier(
    verifier_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_verifier = crud.get_verifier(db, verifier_id=verifier_id)
    if db_verifier is None:
        raise HTTPException(status_code=404, detail="Verifier not found")
    return db_verifier

@router.post("/", response_model=schemas.Verifier)
def create_verifier(
    verifier: schemas.VerifierCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Check if user already has a verifier profile
    existing_verifier = crud.get_verifier_by_user(db, user_id=verifier.user_id)
    if existing_verifier:
        raise HTTPException(status_code=400, detail="User already has a verifier profile")
    
    return crud.create_verifier(db=db, verifier=verifier)

@router.patch("/{verifier_id}", response_model=schemas.Verifier)
def update_verifier(
    verifier_id: int,
    verifier_update: schemas.VerifierUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_verifier = crud.get_verifier(db, verifier_id=verifier_id)
    if db_verifier is None:
        raise HTTPException(status_code=404, detail="Verifier not found")
    
    # Only admin or the verifier themselves can update
    if current_user.role.name != "Administrador" and db_verifier.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud.update_verifier(db=db, verifier_id=verifier_id, verifier_update=verifier_update)
