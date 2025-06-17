from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# Department schemas
class DepartmentBase(BaseModel):
    name: str

class Department(DepartmentBase):
    id: int
    
    class Config:
        from_attributes = True

# Province schemas
class ProvinceBase(BaseModel):
    department_id: int
    name: str

class Province(ProvinceBase):
    id: int
    
    class Config:
        from_attributes = True

class ProvinceWithDepartment(Province):
    department: Department

# District schemas
class DistrictBase(BaseModel):
    province_id: int
    name: str

class District(DistrictBase):
    id: int
    
    class Config:
        from_attributes = True

class DistrictWithProvince(District):
    province: ProvinceWithDepartment

# Role schemas
class RoleBase(BaseModel):
    name: str

class Role(RoleBase):
    id: int
    
    class Config:
        from_attributes = True

# Category schemas
class CategoryBase(BaseModel):
    name: str

class Category(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    first_names: str
    last_names: str
    email: EmailStr
    phone: Optional[str] = None
    gender: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role_id: int

class UserUpdate(BaseModel):
    first_names: Optional[str] = None
    last_names: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    avatar_url: Optional[str] = None

class User(UserBase):
    id: int
    role_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserWithRole(User):
    role: Role

# Organizer schemas
class OrganizerBase(BaseModel):
    document_type: str
    document_number: str
    business_name: Optional[str] = None
    ruc: Optional[str] = None
    work_certificate_file: Optional[str] = None

class OrganizerCreate(OrganizerBase):
    user_id: int

class OrganizerUpdate(BaseModel):
    document_type: Optional[str] = None
    document_number: Optional[str] = None
    business_name: Optional[str] = None
    ruc: Optional[str] = None
    work_certificate_file: Optional[str] = None
    is_approved: Optional[bool] = None

class Organizer(OrganizerBase):
    id: int
    user_id: int
    created_at: datetime
    is_approved: bool
    approval_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class OrganizerWithUser(Organizer):
    user: User

# Verifier schemas
class VerifierBase(BaseModel):
    user_id: int
    organizer_id: int

class VerifierCreate(VerifierBase):
    pass

class VerifierUpdate(BaseModel):
    organizer_id: Optional[int] = None

class Verifier(VerifierBase):
    id: int
    
    class Config:
        from_attributes = True

class VerifierWithDetails(Verifier):
    user: User
    organizer: Organizer

# Event schemas
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    district_id: int
    location_description: Optional[str] = None
    category_id: int
    image_url: Optional[str] = None
    status: str = "active"

class EventCreate(EventBase):
    organizer_id: int
    organizer_user_id: int

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    district_id: Optional[int] = None
    location_description: Optional[str] = None
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    status: Optional[str] = None

class Event(EventBase):
    id: int
    organizer_id: int
    organizer_user_id: int
    
    class Config:
        from_attributes = True

class EventWithDetails(Event):
    district: District
    category: Category
    organizer: Organizer

# EventVerifier schemas
class EventVerifierBase(BaseModel):
    verifier_id: int
    event_id: int

class EventVerifierCreate(EventVerifierBase):
    pass

class EventVerifier(EventVerifierBase):
    id: int
    
    class Config:
        from_attributes = True

# TicketType schemas
class TicketTypeBase(BaseModel):
    event_id: int
    name: str
    price: Decimal
    capacity: int

class TicketTypeCreate(TicketTypeBase):
    pass

class TicketTypeUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None
    capacity: Optional[int] = None

class TicketType(TicketTypeBase):
    id: int
    
    class Config:
        from_attributes = True

# Purchase schemas
class PurchaseBase(BaseModel):
    event_id: int
    user_id: int
    total_amount: Decimal

class PurchaseCreate(PurchaseBase):
    pass

class Purchase(PurchaseBase):
    id: int
    purchase_date: datetime
    
    class Config:
        from_attributes = True

class PurchaseWithDetails(Purchase):
    event: Event
    user: User

# PurchaseDetail schemas
class PurchaseDetailBase(BaseModel):
    purchase_id: int
    ticket_type_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal

class PurchaseDetailCreate(PurchaseDetailBase):
    pass

class PurchaseDetail(PurchaseDetailBase):
    id: int
    
    class Config:
        from_attributes = True

# Ticket schemas
class TicketBase(BaseModel):
    purchase_id: int
    qr_code: str
    status: str = "active"

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    verifier_id: Optional[int] = None
    used_at: Optional[datetime] = None

class Ticket(TicketBase):
    id: int
    created_at: datetime
    used_at: Optional[datetime] = None
    verifier_id: Optional[int] = None
    
    class Config:
        from_attributes = True

# Report schemas
class ReportBase(BaseModel):
    user_id: int
    report_type: str
    description: str

class ReportCreate(ReportBase):
    pass

class ReportUpdate(BaseModel):
    status: Optional[str] = None

class Report(ReportBase):
    id: int
    created_at: datetime
    status: str
    
    class Config:
        from_attributes = True

class ReportWithUser(Report):
    user: User

# ContactUs schemas
class ContactUsBase(BaseModel):
    first_names: str
    last_names: str
    email: EmailStr
    phone: Optional[str] = None
    subject: str
    message: str

class ContactUsCreate(ContactUsBase):
    pass

class ContactUsUpdate(BaseModel):
    status: Optional[str] = None

class ContactUs(ContactUsBase):
    id: int
    created_at: datetime
    status: str
    
    class Config:
        from_attributes = True

# Favorite schemas
class FavoriteBase(BaseModel):
    user_id: int
    event_id: int

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    id: int
    
    class Config:
        from_attributes = True

class FavoriteWithEvent(Favorite):
    event: Event

# Rating schemas
class RatingBase(BaseModel):
    user_id: int
    event_id: int
    score: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int
    
    class Config:
        from_attributes = True

class RatingWithDetails(Rating):
    user: User
    event: Event

# Claim schemas
class ClaimBase(BaseModel):
    first_names: str
    last_names: str
    document_type: str
    document_number: str
    address: str
    district_id: int
    home_phone: Optional[str] = None
    mobile_phone: str
    email: EmailStr
    is_minor: bool = False
    claim_amount: Optional[Decimal] = None
    service_type: str
    product_service_description: str
    claim_type: str
    claim_detail: str
    customer_request: str

class ClaimCreate(ClaimBase):
    pass

class ClaimUpdate(BaseModel):
    status: Optional[str] = None

class Claim(ClaimBase):
    id: int
    created_at: datetime
    status: str
    
    class Config:
        from_attributes = True

class ClaimWithDistrict(Claim):
    district: DistrictWithProvince

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str
