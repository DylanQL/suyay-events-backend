from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, auth

router = APIRouter(prefix="/contact", tags=["contact"])

@router.get("/", response_model=List[schemas.ContactUs])
def read_contact_messages(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_admin_user)
):
    return crud.get_contact_us_list(db, skip=skip, limit=limit)

@router.get("/{contact_id}", response_model=schemas.ContactUs)
def read_contact_message(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_admin_user)
):
    db_contact = crud.get_contact_us(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact message not found")
    return db_contact

@router.post("/", response_model=schemas.ContactUs)
def create_contact_message(
    contact: schemas.ContactUsCreate,
    db: Session = Depends(get_db)
):
    return crud.create_contact_us(db=db, contact=contact)

@router.patch("/{contact_id}", response_model=schemas.ContactUs)
def update_contact_message(
    contact_id: int,
    contact_update: schemas.ContactUsUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_admin_user)
):
    db_contact = crud.get_contact_us(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact message not found")
    
    return crud.update_contact_us(db=db, contact_id=contact_id, contact_update=contact_update)
