from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("/", response_model=List[schemas.Role])
def read_roles(db: Session = Depends(get_db)):
    return crud.get_roles(db)
