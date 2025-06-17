from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, auth

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/", response_model=List[schemas.ReportWithUser])
def read_reports(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Regular users can only see their own reports
    if current_user.role.name != "Administrador" and user_id != current_user.id:
        user_id = current_user.id
    
    return crud.get_reports(db, user_id=user_id, skip=skip, limit=limit)

@router.get("/{report_id}", response_model=schemas.ReportWithUser)
def read_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_report = crud.get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Check if user can access this report
    if current_user.role.name != "Administrador" and db_report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return db_report

@router.post("/", response_model=schemas.Report)
def create_report(
    report: schemas.ReportCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Users can only create reports for themselves
    if current_user.role.name != "Administrador" and report.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Can only create reports for yourself")
    
    return crud.create_report(db=db, report=report)

@router.patch("/{report_id}", response_model=schemas.Report)
def update_report(
    report_id: int,
    report_update: schemas.ReportUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_admin_user)
):
    db_report = crud.get_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return crud.update_report(db=db, report_id=report_id, report_update=report_update)
