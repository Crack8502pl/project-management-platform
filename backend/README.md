# Project Management Platform - Backend

Django REST Framework backend for telecommunications project management platform.

## Features

- **Authentication**: JWT-based authentication with role-based access control
- **Projects**: Project and contract management
- **Tasks**: Task management with multiple types (SMW, CSDIP, LAN PKP PLK, SMOK-IP, SSWiN, SSP, SUG)
- **BOM**: Bill of Materials management with templates and instances
- **Devices**: Network device management with serial numbers
- **IPAM**: IP Address Management with pools and allocations
- **Documents**: Document and photo management
- **Statistics**: Work logs and metrics tracking
- **Installation**: Installation checklists management

## Technology Stack

- Python 3.11+
- Django 5.0+
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- JWT Authentication
- Argon2 password hashing

## Project Structure

```
backend/
├── apps/
│   ├── authentication/      # User authentication and roles
│   ├── projects/           # Project and contract management
│   ├── tasks/              # Task management
│   ├── bom/                # Bill of Materials
│   ├── devices/            # Device management
│   ├── ipam/               # IP Address Management
│   ├── documents/          # Documents and photos
│   ├── statistics/         # Work logs and metrics
│   └── installation/       # Installation checklists
├── config/
│   ├── settings/
│   │   ├── base.py         # Base settings
│   │   ├── development.py  # Development settings
│   │   └── production.py   # Production settings
│   ├── celery.py           # Celery configuration
│   ├── urls.py             # URL routing
│   ├── wsgi.py             # WSGI application
│   └── asgi.py             # ASGI application
├── requirements/
│   ├── base.txt            # Base dependencies
│   └── development.txt     # Development dependencies
├── Dockerfile
├── entrypoint.sh
└── manage.py
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- PostgreSQL 15+ (for local development)
- Redis (for local development)

### Installation with Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd project-management-platform
```

2. Copy environment file:
```bash
cp .env.example .env
```

3. Update `.env` with your configuration (optional, defaults are fine for development)

4. Start the services:
```bash
docker-compose up -d
```

5. The backend will be available at `http://localhost:8000`

6. Access the admin panel at `http://localhost:8000/admin`
   - Default credentials: admin / admin123 (change in `.env`)

7. API documentation:
   - Swagger UI: `http://localhost:8000/api/schema/swagger/`
   - ReDoc: `http://localhost:8000/api/schema/redoc/`

### Local Development Setup

1. Create and activate virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements/development.txt
```

3. Set up environment variables:
```bash
cp ../.env.example ../.env
# Update .env with local database settings
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Initialize roles:
```bash
python manage.py init_roles
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

8. Run Celery worker (in another terminal):
```bash
celery -A config worker --loglevel=info
```

9. Run Celery beat (in another terminal):
```bash
celery -A config beat --loglevel=info
```

## API Endpoints

### Authentication
- `POST /api/auth/token/` - Obtain JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/token/verify/` - Verify JWT token
- `GET /api/auth/users/` - List users
- `POST /api/auth/users/` - Create user
- `GET /api/auth/users/me/` - Get current user
- `PUT /api/auth/users/me/` - Update current user
- `POST /api/auth/users/change_password/` - Change password

### Projects
- `GET /api/projects/` - List projects
- `POST /api/projects/` - Create project
- `GET /api/projects/{id}/` - Get project details
- `PUT /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project
- `GET /api/projects/contracts/` - List contracts
- `POST /api/projects/contracts/` - Create contract

### Tasks
- `GET /api/tasks/` - List tasks
- `POST /api/tasks/` - Create task
- `GET /api/tasks/{id}/` - Get task details
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `POST /api/tasks/{id}/complete/` - Mark task as complete
- `GET /api/tasks/{id}/subtasks/` - Get subtasks

### BOM
- `GET /api/bom/components/` - List components
- `POST /api/bom/components/` - Create component
- `GET /api/bom/templates/` - List BOM templates
- `POST /api/bom/templates/` - Create BOM template
- `GET /api/bom/instances/` - List BOM instances
- `POST /api/bom/instances/` - Create BOM instance

### Devices
- `GET /api/devices/` - List devices
- `POST /api/devices/` - Create device
- `GET /api/devices/{id}/` - Get device details
- `PUT /api/devices/{id}/` - Update device
- `DELETE /api/devices/{id}/` - Delete device

### IPAM
- `GET /api/ipam/pools/` - List IP pools
- `POST /api/ipam/pools/` - Create IP pool
- `GET /api/ipam/addresses/` - List IP addresses
- `POST /api/ipam/addresses/` - Create IP address

### Documents
- `GET /api/documents/documents/` - List documents
- `POST /api/documents/documents/` - Upload document
- `GET /api/documents/photos/` - List photos
- `POST /api/documents/photos/` - Upload photo

### Statistics
- `GET /api/statistics/worklogs/` - List work logs
- `POST /api/statistics/worklogs/` - Create work log
- `GET /api/statistics/metrics/` - List metrics
- `POST /api/statistics/metrics/` - Create metric

### Installation
- `GET /api/installation/checklists/` - List checklists
- `POST /api/installation/checklists/` - Create checklist
- `POST /api/installation/checklists/{id}/complete/` - Complete checklist
- `GET /api/installation/items/` - List checklist items
- `POST /api/installation/items/{id}/toggle_complete/` - Toggle item completion

## User Roles

The system includes the following default roles:

1. **Administrator** - Full system access
2. **Manager** - Project management permissions
3. **Engineer** - Technical permissions
4. **Technician** - Field work permissions
5. **Viewer** - Read-only access

## Task Types

Supported telecommunications task types:

- **SMW** - System Monitoringu Wizyjnego (Video Surveillance System)
- **CSDIP** - Cyfrowy System Dozoru i Przekaźnictwa (Digital Supervision and Relay System)
- **LAN_PKP_PLK** - LAN PKP PLK
- **SMOK_IP** - System Monitoringu i Kontroli IP (IP Monitoring and Control System)
- **SSWiN** - System Sygnalizacji Włamania i Napadu (Intrusion and Burglary Alarm System)
- **SSP** - System Sygnalizacji Pożarowej (Fire Alarm System)
- **SUG** - System Uniwersalnych Gniazd (Universal Socket System)
- **OTHER** - Other task types

## Testing

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=apps --cov-report=html
```

## Code Quality

Format code with Black:
```bash
black .
```

Check code with flake8:
```bash
flake8 .
```

Sort imports with isort:
```bash
isort .
```

## Environment Variables

See `.env.example` for all available environment variables.

Key variables:
- `DEBUG` - Debug mode (True/False)
- `SECRET_KEY` - Django secret key
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host
- `DB_PORT` - Database port
- `CELERY_BROKER_URL` - Celery broker URL
- `CORS_ALLOWED_ORIGINS` - Allowed CORS origins

## Production Deployment

1. Update `.env` with production settings:
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure production database
   - Set proper `ALLOWED_HOSTS`
   - Configure email settings

2. Use production settings:
```bash
export DJANGO_SETTINGS_MODULE=config.settings.production
```

3. Collect static files:
```bash
python manage.py collectstatic --noinput
```

4. Use a production WSGI server (e.g., Gunicorn):
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

5. Set up reverse proxy (e.g., Nginx)

6. Configure HTTPS/SSL

## License

[Your License Here]

## Support

For support, please contact [your-email@example.com]
