from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, auth

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.get("/", response_model=List[schemas.Ticket])
def read_tickets(
    skip: int = 0,
    limit: int = 100,
    purchase_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Regular users can only see their own tickets
    if current_user.role.name not in ["Administrador", "Verificador / Validador de Entrada"] and user_id != current_user.id:
        user_id = current_user.id
    
    return crud.get_tickets(db, purchase_id=purchase_id, user_id=user_id, skip=skip, limit=limit)

@router.get("/{ticket_id}", response_model=schemas.Ticket)
def read_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_ticket = crud.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Check if user can access this ticket
    if current_user.role.name not in ["Administrador", "Verificador / Validador de Entrada"]:
        if db_ticket.purchase.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return db_ticket

@router.get("/qr/{qr_code}", response_model=schemas.Ticket)
def read_ticket_by_qr(
    qr_code: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_verifier_user)
):
    db_ticket = crud.get_ticket_by_qr(db, qr_code=qr_code)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    return db_ticket

@router.post("/", response_model=schemas.Ticket)
def create_ticket(
    purchase_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Verify purchase exists
    db_purchase = crud.get_purchase(db, purchase_id=purchase_id)
    if not db_purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    # Check permissions
    if current_user.role.name != "Administrador" and db_purchase.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud.create_ticket(db=db, purchase_id=purchase_id)

@router.patch("/{ticket_id}", response_model=schemas.Ticket)
def update_ticket(
    ticket_id: int,
    ticket_update: schemas.TicketUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_ticket = crud.get_ticket(db, ticket_id=ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    # Only verifiers and admins can update tickets (for validation)
    if current_user.role.name not in ["Administrador", "Verificador / Validador de Entrada"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud.update_ticket(db=db, ticket_id=ticket_id, ticket_update=ticket_update)
