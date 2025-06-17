# Suyay Events Backend

✅ **PROYECTO COMPLETAMENTE FUNCIONAL** ✅

Backend API for Suyay Events - A comprehensive event management platform built with FastAPI and SQLAlchemy.

## 🚀 Status del Proyecto

- ✅ Entorno virtual configurado
- ✅ Base de datos MySQL conectada y funcionando
- ✅ Todas las tablas creadas automáticamente
- ✅ Datos iniciales cargados (roles, categorías, ubicaciones)
- ✅ Servidor ejecutándose en http://localhost:8000
- ✅ Documentación interactiva disponible en http://localhost:8000/docs
- ✅ Autenticación JWT implementada
- ✅ Control de roles funcional
- ✅ Todos los endpoints CRUD implementados

## 🎯 Características Implementadas

- **User Management**: Registration, authentication, and role-based access control
- **Event Management**: Create, update, delete, and view events
- **Ticket System**: Ticket types, purchases, and QR code generation
- **Organizer Profiles**: Organizer registration and approval system
- **Verification System**: Event verifiers for ticket validation
- **Location System**: Departments, provinces, and districts (Peru)
- **Rating & Reviews**: Users can rate and review events
- **Favorites**: Users can mark events as favorites
- **Reports & Claims**: User reports and customer claims system
- **Contact System**: Contact form for customer support

## User Roles

1. **Administrador** (Administrator) - Web platform access
2. **Organizador de Eventos** (Event Organizer) - Web platform access
3. **Comprador / Asistente** (Buyer/Attendee) - Web and mobile access
4. **Verificador / Validador de Entrada** (Ticket Verifier) - Mobile access

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **MySQL**: Database
- **JWT**: Authentication
- **Pydantic**: Data validation
- **Alembic**: Database migrations
- **Uvicorn**: ASGI server

## Database Configuration

The application connects to MySQL with the following configuration:
- Server: mysql1002.site4now.net
- Database: db_aba258_suyay
- User: aba258_suyay

## 🚀 Inicio Rápido

El proyecto está listo para usar. El servidor está ejecutándose en:

- **API Base URL**: http://localhost:8000
- **Documentación Interactiva**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

### Comandos disponibles:

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar servidor
python main.py

# Inicializar base de datos (ya ejecutado)
python init_db.py
```

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env` file:
```
DATABASE_URL=mysql+pymysql://aba258_suyay:Holamundo666@mysql1002.site4now.net/db_aba258_suyay
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload
```

## API Documentation

Once the server is running, you can access:
- Interactive API docs: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/me` - Get current user info

### Users
- `GET /users/` - Get all users (Admin only)
- `GET /users/{user_id}` - Get user by ID
- `PATCH /users/{user_id}` - Update user

### Locations
- `GET /locations/departments` - Get all departments
- `GET /locations/provinces` - Get provinces (optionally by department)
- `GET /locations/districts` - Get districts (optionally by province)

### Categories & Roles
- `GET /categories/` - Get all event categories
- `GET /roles/` - Get all user roles

### Events
- `GET /events/` - Get all events
- `GET /events/{event_id}` - Get event by ID
- `POST /events/` - Create new event (Organizer only)
- `PATCH /events/{event_id}` - Update event
- `DELETE /events/{event_id}` - Delete event

### Organizers
- `GET /organizers/` - Get all organizers
- `GET /organizers/{organizer_id}` - Get organizer by ID
- `POST /organizers/` - Create organizer profile
- `PATCH /organizers/{organizer_id}` - Update organizer

### Ticket Management
- `GET /ticket-types/` - Get ticket types
- `POST /ticket-types/` - Create ticket type
- `PATCH /ticket-types/{ticket_type_id}` - Update ticket type
- `DELETE /ticket-types/{ticket_type_id}` - Delete ticket type

### Purchases & Tickets
- `GET /purchases/` - Get purchases
- `POST /purchases/` - Create purchase
- `GET /tickets/` - Get tickets
- `GET /tickets/qr/{qr_code}` - Get ticket by QR code (Verifier only)

### Additional Features
- Favorites management
- Ratings and reviews
- Reports system
- Claims management
- Contact form

## Database Schema

The application includes the following main entities:

- **Users**: User accounts with role-based access
- **Events**: Event information and management
- **Tickets**: Ticket system with QR codes
- **Purchases**: Purchase transactions and details
- **Organizers**: Event organizer profiles
- **Verifiers**: Ticket verification personnel
- **Locations**: Geographic data (departments, provinces, districts)
- **Categories**: Event categorization
- **Reports**: User reports and feedback
- **Claims**: Customer claims and complaints

## Security

- JWT-based authentication
- Role-based access control
- Password hashing with bcrypt
- Input validation with Pydantic

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is proprietary and confidential.
