from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/locations", tags=["locations"])

@router.get("/departments", response_model=List[schemas.Department])
def read_departments(db: Session = Depends(get_db)):
    return crud.get_departments(db)

@router.get("/provinces", response_model=List[schemas.ProvinceWithDepartment])
def read_provinces(
    department_id: int = None,
    db: Session = Depends(get_db)
):
    return crud.get_provinces(db, department_id=department_id)

@router.get("/districts", response_model=List[schemas.District])
def read_districts(
    province_id: int = None,
    db: Session = Depends(get_db)
):
    return crud.get_districts(db, province_id=province_id)
