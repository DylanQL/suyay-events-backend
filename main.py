from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base
from app.routers import (
    auth, users, locations, categories, roles, organizers, 
    verifiers, events, event_verifiers, ticket_types, 
    purchases, purchase_details, tickets, reports, 
    contact, favorites, ratings, claims
)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Suyay Events API",
    description="API for Suyay Events - Event Management Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(locations.router)
app.include_router(categories.router)
app.include_router(roles.router)
app.include_router(organizers.router)
app.include_router(verifiers.router)
app.include_router(events.router)
app.include_router(event_verifiers.router)
app.include_router(ticket_types.router)
app.include_router(purchases.router)
app.include_router(purchase_details.router)
app.include_router(tickets.router)
app.include_router(reports.router)
app.include_router(contact.router)
app.include_router(favorites.router)
app.include_router(ratings.router)
app.include_router(claims.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Suyay Events API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        reload=True,  # Auto-reload en desarrollo
        log_level="info"
    )
