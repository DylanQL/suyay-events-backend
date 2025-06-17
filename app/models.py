from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    
    provinces = relationship("Province", back_populates="department")

class Province(Base):
    __tablename__ = "provinces"
    
    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    name = Column(String(100), nullable=False)
    
    department = relationship("Department", back_populates="provinces")
    districts = relationship("District", back_populates="province")

class District(Base):
    __tablename__ = "districts"
    
    id = Column(Integer, primary_key=True, index=True)
    province_id = Column(Integer, ForeignKey("provinces.id"), nullable=False)
    name = Column(String(100), nullable=False)
    
    province = relationship("Province", back_populates="districts")
    events = relationship("Event", back_populates="district")
    claims = relationship("Claim", back_populates="district")

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    
    users = relationship("User", back_populates="role")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    
    events = relationship("Event", back_populates="category")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_names = Column(String(100), nullable=False)
    last_names = Column(String(100), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    gender = Column(String(20), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    role = relationship("Role", back_populates="users")
    organizer = relationship("Organizer", back_populates="user", uselist=False)
    verifier = relationship("Verifier", back_populates="user", uselist=False)
    events = relationship("Event", back_populates="organizer_user")
    purchases = relationship("Purchase", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")
    ratings = relationship("Rating", back_populates="user")
    reports = relationship("Report", back_populates="user")

class Organizer(Base):
    __tablename__ = "organizers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    document_type = Column(String(50), nullable=False)
    document_number = Column(String(50), nullable=False)
    business_name = Column(String(200), nullable=True)
    ruc = Column(String(20), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    work_certificate_file = Column(String(500), nullable=True)
    is_approved = Column(Boolean, default=False, nullable=False)
    approval_date = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="organizer")
    events = relationship("Event", back_populates="organizer")
    verifiers = relationship("Verifier", back_populates="organizer")

class Verifier(Base):
    __tablename__ = "verifiers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    organizer_id = Column(Integer, ForeignKey("organizers.id"), nullable=False)
    
    user = relationship("User", back_populates="verifier")
    organizer = relationship("Organizer", back_populates="verifiers")
    event_verifiers = relationship("EventVerifier", back_populates="verifier")
    tickets = relationship("Ticket", back_populates="verifier")

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    location_description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    organizer_id = Column(Integer, ForeignKey("organizers.id"), nullable=False)
    organizer_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image_url = Column(String(500), nullable=True)
    status = Column(String(50), default="active", nullable=False)
    
    district = relationship("District", back_populates="events")
    category = relationship("Category", back_populates="events")
    organizer = relationship("Organizer", back_populates="events")
    organizer_user = relationship("User", back_populates="events")
    ticket_types = relationship("TicketType", back_populates="event")
    purchases = relationship("Purchase", back_populates="event")
    favorites = relationship("Favorite", back_populates="event")
    ratings = relationship("Rating", back_populates="event")
    event_verifiers = relationship("EventVerifier", back_populates="event")

class EventVerifier(Base):
    __tablename__ = "event_verifiers"
    
    id = Column(Integer, primary_key=True, index=True)
    verifier_id = Column(Integer, ForeignKey("verifiers.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    
    verifier = relationship("Verifier", back_populates="event_verifiers")
    event = relationship("Event", back_populates="event_verifiers")

class TicketType(Base):
    __tablename__ = "ticket_types"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    capacity = Column(Integer, nullable=False)
    
    event = relationship("Event", back_populates="ticket_types")
    purchase_details = relationship("PurchaseDetail", back_populates="ticket_type")

class Purchase(Base):
    __tablename__ = "purchases"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    purchase_date = Column(DateTime, server_default=func.now(), nullable=False)
    
    event = relationship("Event", back_populates="purchases")
    user = relationship("User", back_populates="purchases")
    details = relationship("PurchaseDetail", back_populates="purchase")
    tickets = relationship("Ticket", back_populates="purchase")

class PurchaseDetail(Base):
    __tablename__ = "purchase_details"
    
    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"), nullable=False)
    ticket_type_id = Column(Integer, ForeignKey("ticket_types.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    
    purchase = relationship("Purchase", back_populates="details")
    ticket_type = relationship("TicketType", back_populates="purchase_details")

class Ticket(Base):
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey("purchases.id"), nullable=False)
    qr_code = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    used_at = Column(DateTime, nullable=True)
    status = Column(String(50), default="active", nullable=False)  # active, used, expired
    verifier_id = Column(Integer, ForeignKey("verifiers.id"), nullable=True)
    
    purchase = relationship("Purchase", back_populates="tickets")
    verifier = relationship("Verifier", back_populates="tickets")

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    
    user = relationship("User", back_populates="reports")

class ContactUs(Base):
    __tablename__ = "contact_us"
    
    id = Column(Integer, primary_key=True, index=True)
    first_names = Column(String(100), nullable=False)
    last_names = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(String(50), default="pending", nullable=False)

class Favorite(Base):
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    
    user = relationship("User", back_populates="favorites")
    event = relationship("Event", back_populates="favorites")

class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    score = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text, nullable=True)
    
    user = relationship("User", back_populates="ratings")
    event = relationship("Event", back_populates="ratings")

class Claim(Base):
    __tablename__ = "claims"
    
    id = Column(Integer, primary_key=True, index=True)
    first_names = Column(String(100), nullable=False)
    last_names = Column(String(100), nullable=False)
    document_type = Column(String(50), nullable=False)
    document_number = Column(String(50), nullable=False)
    address = Column(Text, nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    home_phone = Column(String(20), nullable=True)
    mobile_phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    is_minor = Column(Boolean, default=False, nullable=False)
    claim_amount = Column(Numeric(10, 2), nullable=True)
    service_type = Column(String(100), nullable=False)
    product_service_description = Column(Text, nullable=False)
    claim_type = Column(String(100), nullable=False)
    claim_detail = Column(Text, nullable=False)
    customer_request = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    status = Column(String(50), default="pending", nullable=False)
    
    district = relationship("District", back_populates="claims")
