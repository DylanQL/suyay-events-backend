from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from app import models, schemas
from app.auth import get_password_hash
import secrets
import string

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_names=user.first_names,
        last_names=user.last_names,
        email=user.email,
        password=hashed_password,
        phone=user.phone,
        role_id=user.role_id,
        gender=user.gender,
        avatar_url=user.avatar_url
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user

# Role CRUD
def get_roles(db: Session):
    return db.query(models.Role).all()

def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()

# Category CRUD
def get_categories(db: Session):
    return db.query(models.Category).all()

def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

# Department, Province, District CRUD
def get_departments(db: Session):
    return db.query(models.Department).all()

def get_provinces(db: Session, department_id: Optional[int] = None):
    query = db.query(models.Province)
    if department_id:
        query = query.filter(models.Province.department_id == department_id)
    return query.all()

def get_districts(db: Session, province_id: Optional[int] = None):
    query = db.query(models.District)
    if province_id:
        query = query.filter(models.District.province_id == province_id)
    return query.all()

# Organizer CRUD
def get_organizer(db: Session, organizer_id: int):
    return db.query(models.Organizer).filter(models.Organizer.id == organizer_id).first()

def get_organizer_by_user(db: Session, user_id: int):
    return db.query(models.Organizer).filter(models.Organizer.user_id == user_id).first()

def get_organizers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Organizer).offset(skip).limit(limit).all()

def create_organizer(db: Session, organizer: schemas.OrganizerCreate):
    db_organizer = models.Organizer(**organizer.dict())
    db.add(db_organizer)
    db.commit()
    db.refresh(db_organizer)
    return db_organizer

def update_organizer(db: Session, organizer_id: int, organizer_update: schemas.OrganizerUpdate):
    db_organizer = db.query(models.Organizer).filter(models.Organizer.id == organizer_id).first()
    if db_organizer:
        update_data = organizer_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_organizer, field, value)
        db.commit()
        db.refresh(db_organizer)
    return db_organizer

# Verifier CRUD
def get_verifier(db: Session, verifier_id: int):
    return db.query(models.Verifier).filter(models.Verifier.id == verifier_id).first()

def get_verifier_by_user(db: Session, user_id: int):
    return db.query(models.Verifier).filter(models.Verifier.user_id == user_id).first()

def get_verifiers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Verifier).offset(skip).limit(limit).all()

def create_verifier(db: Session, verifier: schemas.VerifierCreate):
    db_verifier = models.Verifier(**verifier.dict())
    db.add(db_verifier)
    db.commit()
    db.refresh(db_verifier)
    return db_verifier

def update_verifier(db: Session, verifier_id: int, verifier_update: schemas.VerifierUpdate):
    db_verifier = db.query(models.Verifier).filter(models.Verifier.id == verifier_id).first()
    if db_verifier:
        update_data = verifier_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_verifier, field, value)
        db.commit()
        db.refresh(db_verifier)
    return db_verifier

# Event CRUD
def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None, organizer_id: Optional[int] = None):
    query = db.query(models.Event)
    if category_id:
        query = query.filter(models.Event.category_id == category_id)
    if organizer_id:
        query = query.filter(models.Event.organizer_id == organizer_id)
    return query.offset(skip).limit(limit).all()

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event_update: schemas.EventUpdate):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        update_data = event_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_event, field, value)
        db.commit()
        db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event

# EventVerifier CRUD
def get_event_verifiers(db: Session, event_id: Optional[int] = None, verifier_id: Optional[int] = None):
    query = db.query(models.EventVerifier)
    if event_id:
        query = query.filter(models.EventVerifier.event_id == event_id)
    if verifier_id:
        query = query.filter(models.EventVerifier.verifier_id == verifier_id)
    return query.all()

def create_event_verifier(db: Session, event_verifier: schemas.EventVerifierCreate):
    db_event_verifier = models.EventVerifier(**event_verifier.dict())
    db.add(db_event_verifier)
    db.commit()
    db.refresh(db_event_verifier)
    return db_event_verifier

def delete_event_verifier(db: Session, event_verifier_id: int):
    db_event_verifier = db.query(models.EventVerifier).filter(models.EventVerifier.id == event_verifier_id).first()
    if db_event_verifier:
        db.delete(db_event_verifier)
        db.commit()
    return db_event_verifier

# TicketType CRUD
def get_ticket_type(db: Session, ticket_type_id: int):
    return db.query(models.TicketType).filter(models.TicketType.id == ticket_type_id).first()

def get_ticket_types(db: Session, event_id: Optional[int] = None):
    query = db.query(models.TicketType)
    if event_id:
        query = query.filter(models.TicketType.event_id == event_id)
    return query.all()

def create_ticket_type(db: Session, ticket_type: schemas.TicketTypeCreate):
    db_ticket_type = models.TicketType(**ticket_type.dict())
    db.add(db_ticket_type)
    db.commit()
    db.refresh(db_ticket_type)
    return db_ticket_type

def update_ticket_type(db: Session, ticket_type_id: int, ticket_type_update: schemas.TicketTypeUpdate):
    db_ticket_type = db.query(models.TicketType).filter(models.TicketType.id == ticket_type_id).first()
    if db_ticket_type:
        update_data = ticket_type_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ticket_type, field, value)
        db.commit()
        db.refresh(db_ticket_type)
    return db_ticket_type

def delete_ticket_type(db: Session, ticket_type_id: int):
    db_ticket_type = db.query(models.TicketType).filter(models.TicketType.id == ticket_type_id).first()
    if db_ticket_type:
        db.delete(db_ticket_type)
        db.commit()
    return db_ticket_type

# Purchase CRUD
def get_purchase(db: Session, purchase_id: int):
    return db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()

def get_purchases(db: Session, user_id: Optional[int] = None, event_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Purchase)
    if user_id:
        query = query.filter(models.Purchase.user_id == user_id)
    if event_id:
        query = query.filter(models.Purchase.event_id == event_id)
    return query.offset(skip).limit(limit).all()

def create_purchase(db: Session, purchase: schemas.PurchaseCreate):
    db_purchase = models.Purchase(**purchase.dict())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

# PurchaseDetail CRUD
def get_purchase_details(db: Session, purchase_id: int):
    return db.query(models.PurchaseDetail).filter(models.PurchaseDetail.purchase_id == purchase_id).all()

def create_purchase_detail(db: Session, purchase_detail: schemas.PurchaseDetailCreate):
    db_purchase_detail = models.PurchaseDetail(**purchase_detail.dict())
    db.add(db_purchase_detail)
    db.commit()
    db.refresh(db_purchase_detail)
    return db_purchase_detail

# Ticket CRUD
def generate_qr_code():
    """Generate a unique QR code string"""
    return ''.join(secrets.choice(string.digits) for _ in range(12))

def get_ticket(db: Session, ticket_id: int):
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

def get_ticket_by_qr(db: Session, qr_code: str):
    return db.query(models.Ticket).filter(models.Ticket.qr_code == qr_code).first()

def get_tickets(db: Session, purchase_id: Optional[int] = None, user_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Ticket)
    if purchase_id:
        query = query.filter(models.Ticket.purchase_id == purchase_id)
    if user_id:
        query = query.join(models.Purchase).filter(models.Purchase.user_id == user_id)
    return query.offset(skip).limit(limit).all()

def create_ticket(db: Session, purchase_id: int):
    qr_code = generate_qr_code()
    # Ensure QR code is unique
    while db.query(models.Ticket).filter(models.Ticket.qr_code == qr_code).first():
        qr_code = generate_qr_code()
    
    db_ticket = models.Ticket(
        purchase_id=purchase_id,
        qr_code=qr_code,
        status="active"
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def update_ticket(db: Session, ticket_id: int, ticket_update: schemas.TicketUpdate):
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if db_ticket:
        update_data = ticket_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_ticket, field, value)
        db.commit()
        db.refresh(db_ticket)
    return db_ticket

# Report CRUD
def get_report(db: Session, report_id: int):
    return db.query(models.Report).filter(models.Report.id == report_id).first()

def get_reports(db: Session, user_id: Optional[int] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Report)
    if user_id:
        query = query.filter(models.Report.user_id == user_id)
    return query.offset(skip).limit(limit).all()

def create_report(db: Session, report: schemas.ReportCreate):
    db_report = models.Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def update_report(db: Session, report_id: int, report_update: schemas.ReportUpdate):
    db_report = db.query(models.Report).filter(models.Report.id == report_id).first()
    if db_report:
        update_data = report_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_report, field, value)
        db.commit()
        db.refresh(db_report)
    return db_report

# ContactUs CRUD
def get_contact_us(db: Session, contact_id: int):
    return db.query(models.ContactUs).filter(models.ContactUs.id == contact_id).first()

def get_contact_us_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ContactUs).offset(skip).limit(limit).all()

def create_contact_us(db: Session, contact: schemas.ContactUsCreate):
    db_contact = models.ContactUs(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact_us(db: Session, contact_id: int, contact_update: schemas.ContactUsUpdate):
    db_contact = db.query(models.ContactUs).filter(models.ContactUs.id == contact_id).first()
    if db_contact:
        update_data = contact_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_contact, field, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

# Favorite CRUD
def get_favorite(db: Session, user_id: int, event_id: int):
    return db.query(models.Favorite).filter(
        and_(models.Favorite.user_id == user_id, models.Favorite.event_id == event_id)
    ).first()

def get_favorites(db: Session, user_id: int):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user_id).all()

def create_favorite(db: Session, favorite: schemas.FavoriteCreate):
    db_favorite = models.Favorite(**favorite.dict())
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def delete_favorite(db: Session, favorite_id: int):
    db_favorite = db.query(models.Favorite).filter(models.Favorite.id == favorite_id).first()
    if db_favorite:
        db.delete(db_favorite)
        db.commit()
    return db_favorite

# Rating CRUD
def get_rating(db: Session, user_id: int, event_id: int):
    return db.query(models.Rating).filter(
        and_(models.Rating.user_id == user_id, models.Rating.event_id == event_id)
    ).first()

def get_ratings(db: Session, event_id: Optional[int] = None, user_id: Optional[int] = None):
    query = db.query(models.Rating)
    if event_id:
        query = query.filter(models.Rating.event_id == event_id)
    if user_id:
        query = query.filter(models.Rating.user_id == user_id)
    return query.all()

def create_rating(db: Session, rating: schemas.RatingCreate):
    db_rating = models.Rating(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

# Claim CRUD
def get_claim(db: Session, claim_id: int):
    return db.query(models.Claim).filter(models.Claim.id == claim_id).first()

def get_claims(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Claim).offset(skip).limit(limit).all()

def create_claim(db: Session, claim: schemas.ClaimCreate):
    db_claim = models.Claim(**claim.dict())
    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)
    return db_claim

def update_claim(db: Session, claim_id: int, claim_update: schemas.ClaimUpdate):
    db_claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()
    if db_claim:
        update_data = claim_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_claim, field, value)
        db.commit()
        db.refresh(db_claim)
    return db_claim
