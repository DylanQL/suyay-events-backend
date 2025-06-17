"""
Initialize database with basic data
"""
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Role, Category, Department, Province, District
from app import crud, schemas

def init_db():
    """Initialize database with basic data"""
    db = SessionLocal()
    
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        # Initialize Roles
        roles = [
            "Administrador",
            "Organizador de Eventos", 
            "Comprador / Asistente",
            "Verificador / Validador de Entrada"
        ]
        
        for role_name in roles:
            existing_role = db.query(Role).filter(Role.name == role_name).first()
            if not existing_role:
                db_role = Role(name=role_name)
                db.add(db_role)
        
        # Initialize Categories
        categories = [
            "Conciertos",
            "Conferencias",
            "Deportes",
            "Teatro",
            "Exposiciones",
            "Festivales",
            "Talleres",
            "Seminarios"
        ]
        
        for category_name in categories:
            existing_category = db.query(Category).filter(Category.name == category_name).first()
            if not existing_category:
                db_category = Category(name=category_name)
                db.add(db_category)
        
        # Initialize basic location data (Peru)
        departments_data = [
            {"name": "Lima", "provinces": [
                {"name": "Lima", "districts": ["Lima", "Miraflores", "San Isidro", "Barranco", "Surco"]},
                {"name": "Callao", "districts": ["Callao", "Bellavista", "Carmen de la Legua"]}
            ]},
            {"name": "Arequipa", "provinces": [
                {"name": "Arequipa", "districts": ["Arequipa", "Cayma", "Cerro Colorado", "Paucarpata"]}
            ]},
            {"name": "Cusco", "provinces": [
                {"name": "Cusco", "districts": ["Cusco", "San Blas", "San Sebastián"]}
            ]}
        ]
        
        for dept_data in departments_data:
            existing_dept = db.query(Department).filter(Department.name == dept_data["name"]).first()
            if not existing_dept:
                db_dept = Department(name=dept_data["name"])
                db.add(db_dept)
                db.commit()
                db.refresh(db_dept)
                
                for prov_data in dept_data["provinces"]:
                    db_prov = Province(name=prov_data["name"], department_id=db_dept.id)
                    db.add(db_prov)
                    db.commit()
                    db.refresh(db_prov)
                    
                    for district_name in prov_data["districts"]:
                        db_district = District(name=district_name, province_id=db_prov.id)
                        db.add(db_district)
        
        db.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
