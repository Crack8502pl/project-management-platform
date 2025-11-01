# Project Management Platform

Platform zarządzania projektami telekomunikacyjnymi - SMW, CSDIP, LAN PKP PLK, SMOK-IP, SSWiN, SSP, SUG

A comprehensive project management platform for telecommunications projects with support for various task types, Bill of Materials, device management, IP address management, documentation, and installation checklists.

## Features

### Backend (Django REST Framework)
- JWT-based authentication with role-based access control
- Project and contract management
- Task management with multiple telecommunications task types
- Bill of Materials (BOM) with templates and instances
- Device management with serial numbers and configurations
- IP Address Management (IPAM) with pools and allocations
- Document and photo management
- Work log and metrics tracking
- Installation checklist management
- Celery for asynchronous task processing
- API documentation with Swagger/ReDoc

### Frontend (React + TypeScript)
- Modern React application with TypeScript
- Integration with Django REST API
- [See frontend/README.md for details]

## Project Structure

```
project-management-platform/
├── backend/              # Django REST Framework backend
│   ├── apps/            # Django applications
│   ├── config/          # Django configuration
│   ├── requirements/    # Python dependencies
│   ├── Dockerfile
│   └── README.md
├── frontend/            # React frontend
│   └── README.md
├── docker-compose.yml   # Docker Compose configuration
└── .env.example         # Environment variables template
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd project-management-platform
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Start all services with Docker Compose:
```bash
docker-compose up -d
```

4. Access the applications:
   - Backend API: http://localhost:8000
   - Backend Admin: http://localhost:8000/admin (admin/admin123)
   - API Documentation: http://localhost:8000/api/schema/swagger/
   - Frontend: http://localhost:3000 (if configured)

### Default Credentials

- **Username**: admin
- **Password**: admin123

⚠️ **Important**: Change these credentials in production!

## Development Setup

### Backend Development

See [backend/README.md](backend/README.md) for detailed backend setup instructions.

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements/development.txt
python manage.py migrate
python manage.py init_roles
python manage.py runserver
```

### Frontend Development

See [frontend/README.md](frontend/README.md) for detailed frontend setup instructions.

```bash
cd frontend
npm install
npm start
```

## Technology Stack

### Backend
- Python 3.11+
- Django 5.0+
- Django REST Framework
- PostgreSQL 15
- Redis 7
- Celery
- JWT Authentication (djangorestframework-simplejwt)
- Argon2 password hashing
- drf-spectacular for API documentation

### Frontend
- React 18+
- TypeScript
- [Additional frontend technologies]

## API Documentation

API documentation is available at:
- Swagger UI: http://localhost:8000/api/schema/swagger/
- ReDoc: http://localhost:8000/api/schema/redoc/
- OpenAPI Schema: http://localhost:8000/api/schema/

## User Roles

The platform supports the following user roles:

1. **Administrator** - Full system access and configuration
2. **Manager** - Project management and team coordination
3. **Engineer** - Technical task management and device configuration
4. **Technician** - Field work and checklist management
5. **Viewer** - Read-only access to projects and documentation

## Task Types

The platform supports various telecommunications task types:

- **SMW** - System Monitoringu Wizyjnego (Video Surveillance System)
- **CSDIP** - Cyfrowy System Dozoru i Przekaźnictwa
- **LAN PKP PLK** - Railway LAN Network
- **SMOK-IP** - System Monitoringu i Kontroli IP
- **SSWiN** - System Sygnalizacji Włamania i Napadu
- **SSP** - System Sygnalizacji Pożarowej
- **SUG** - System Uniwersalnych Gniazd
- **Other** - Custom task types

## Environment Variables

Key environment variables (see `.env.example` for complete list):

```env
# Django
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=project_management
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Redis/Celery
CELERY_BROKER_URL=redis://redis:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Superuser
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123
```

## Docker Services

The docker-compose configuration includes:

- **db** - PostgreSQL database
- **redis** - Redis for Celery
- **backend** - Django REST Framework API
- **celery** - Celery worker for async tasks
- **celery-beat** - Celery beat for scheduled tasks

## Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=apps --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Production Deployment

For production deployment:

1. Update `.env` with production values
2. Set `DEBUG=False`
3. Use strong `SECRET_KEY`
4. Configure production database
5. Set up proper `ALLOWED_HOSTS`
6. Configure email settings
7. Use HTTPS/SSL
8. Set up reverse proxy (Nginx)
9. Use production WSGI server (Gunicorn)

See backend/README.md for detailed production deployment instructions.

## Contributing

[Add contributing guidelines]

## License

[Add license information]

## Support

For support, please contact [your-email@example.com]
