from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, auth

router = APIRouter(prefix="/ticket-types", tags=["ticket-types"])

@router.get("/", response_model=List[schemas.TicketType])
def read_ticket_types(
    event_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_ticket_types(db, event_id=event_id)

@router.get("/{ticket_type_id}", response_model=schemas.TicketType)
def read_ticket_type(
    ticket_type_id: int,
    db: Session = Depends(get_db)
):
    db_ticket_type = crud.get_ticket_type(db, ticket_type_id=ticket_type_id)
    if db_ticket_type is None:
        raise HTTPException(status_code=404, detail="Ticket type not found")
    return db_ticket_type

@router.post("/", response_model=schemas.TicketType)
def create_ticket_type(
    ticket_type: schemas.TicketTypeCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    # Check if event exists and user has permission
    db_event = crud.get_event(db, event_id=ticket_type.event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Only admin or event organizer can create ticket types
    if current_user.role.name != "Administrador" and db_event.organizer_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud.create_ticket_type(db=db, ticket_type=ticket_type)

@router.patch("/{ticket_type_id}", response_model=schemas.TicketType)
def update_ticket_type(
    ticket_type_id: int,
    ticket_type_update: schemas.TicketTypeUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_ticket_type = crud.get_ticket_type(db, ticket_type_id=ticket_type_id)
    if db_ticket_type is None:
        raise HTTPException(status_code=404, detail="Ticket type not found")
    
    # Check event ownership
    db_event = crud.get_event(db, event_id=db_ticket_type.event_id)
    if current_user.role.name != "Administrador" and db_event.organizer_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return crud.update_ticket_type(db=db, ticket_type_id=ticket_type_id, ticket_type_update=ticket_type_update)

@router.delete("/{ticket_type_id}")
def delete_ticket_type(
    ticket_type_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_ticket_type = crud.get_ticket_type(db, ticket_type_id=ticket_type_id)
    if db_ticket_type is None:
        raise HTTPException(status_code=404, detail="Ticket type not found")
    
    # Check event ownership
    db_event = crud.get_event(db, event_id=db_ticket_type.event_id)
    if current_user.role.name != "Administrador" and db_event.organizer_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    crud.delete_ticket_type(db=db, ticket_type_id=ticket_type_id)
    return {"message": "Ticket type deleted successfully"}
