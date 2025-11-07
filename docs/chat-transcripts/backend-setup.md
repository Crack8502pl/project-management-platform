# Backend Setup Guide

Extracted from chat transcript - step-by-step backend initialization and configuration.

---

## Overview

This guide provides complete instructions for initializing and running the Django backend for the Project Management Platform, including database setup, migrations, user creation, and testing.

---

## Prerequisites

- Docker and Docker Compose installed
- `.env` file configured (copy from `.env.example`)
- Docker Desktop running (if on Windows/Mac)

---

## Initial Setup Steps

### Step 1: Copy Environment Configuration

The backend requires environment variables to be set. Start by copying the example file:

```bash
# From the root directory of the project
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# Use your preferred editor
nano .env
# or
vim .env
# or
code .env
```

**Minimum required variables:**
```env
DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=project_management
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123
```

### Step 2: Start Docker Services

Start all services using Docker Compose:

```bash
docker-compose up -d
```

This will start:
- **db** - PostgreSQL database
- **redis** - Redis for Celery
- **backend** - Django application
- **celery** - Celery worker (if configured)
- **celery-beat** - Celery beat scheduler (if configured)

Check that services are running:
```bash
docker-compose ps
```

Expected output:
```
NAME                COMMAND                  STATUS
backend             "python manage.py ru…"   Up
db                  "docker-entrypoint.s…"   Up
redis               "docker-entrypoint.s…"   Up
```

### Step 3: Run Database Migrations

Apply all database migrations to create the necessary tables:

```bash
docker-compose exec backend python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, users, projects, tasks, bom, devices, ipam, documents, worklogs, checklists
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### Step 4: Initialize User Roles

Create the predefined user roles (Administrator, Manager, Engineer, Technician, Viewer):

```bash
docker-compose exec backend python manage.py init_roles
```

Expected output:
```
Creating roles...
✓ Role 'Administrator' created
✓ Role 'Manager' created
✓ Role 'Engineer' created
✓ Role 'Technician' created
✓ Role 'Viewer' created
Roles initialized successfully!
```

### Step 5: Create Superuser

Create an administrative user to access Django Admin:

**Option A: Interactive creation**
```bash
docker-compose exec backend python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.
```

**Option B: Using environment variables**

If you set the superuser credentials in `.env`, they should be automatically created on first run. Verify by trying to log in.

### Step 6: Verify Backend is Running

Check that the backend is accessible:

```bash
curl http://localhost:8000/api/
```

Or open in browser: http://localhost:8000/api/

---

## Accessing the Application

### Django Admin Panel

- **URL:** http://localhost:8000/admin
- **Default credentials:** 
  - Username: `admin` (or as configured in `.env`)
  - Password: `admin123` (or as configured in `.env`)

**Important:** Change default credentials for production!

### API Documentation

The API documentation is available at multiple endpoints:

- **Swagger UI:** http://localhost:8000/api/schema/swagger/
  - Interactive API documentation
  - Test endpoints directly from the browser
  - View request/response schemas

- **ReDoc:** http://localhost:8000/api/schema/redoc/
  - Alternative API documentation UI
  - Better for reading and printing

- **OpenAPI Schema:** http://localhost:8000/api/schema/
  - Raw OpenAPI 3.0 schema in JSON/YAML
  - Use for code generation tools

---

## Key API Endpoints

### Authentication Endpoints

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "",
    "last_name": "",
    "role": {
      "id": 1,
      "name": "Administrator"
    }
  }
}
```

#### Refresh Token
```http
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Verify Token
```http
POST /api/auth/verify/
Content-Type: application/json

{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### User Endpoints

```http
GET /api/users/              # List all users
GET /api/users/{id}/         # Get user details
POST /api/users/             # Create user
PUT /api/users/{id}/         # Update user
PATCH /api/users/{id}/       # Partial update
DELETE /api/users/{id}/      # Delete user
```

### Project Endpoints

```http
GET /api/projects/           # List all projects
POST /api/projects/          # Create project
GET /api/projects/{id}/      # Get project details
PUT /api/projects/{id}/      # Update project
DELETE /api/projects/{id}/   # Delete project
```

### Task Endpoints

```http
GET /api/tasks/              # List all tasks
POST /api/tasks/             # Create task
GET /api/tasks/{id}/         # Get task details
PUT /api/tasks/{id}/         # Update task
DELETE /api/tasks/{id}/      # Delete task
```

For a complete list of endpoints, see:
- API_ENDPOINTS.md in the repository root
- Swagger documentation at http://localhost:8000/api/schema/swagger/

---

## LDAP Configuration (Optional)

If you want to enable LDAP/Active Directory authentication:

### Configure LDAP Environment Variables

Add to your `.env` file:

```env
# LDAP/Active Directory Configuration
LDAP_SERVER_URI=ldap://dc.example.local:389
LDAP_BIND_DN=CN=Service Account,OU=ServiceAccounts,DC=example,DC=local
LDAP_BIND_PASSWORD=[REDACTED]
LDAP_USER_SEARCH_BASE=CN=Users,DC=example,DC=local
```

### LDAP Settings Location

LDAP configuration is in Django settings files:
- Development: `backend/config/settings/development.py`
- Production: `backend/config/settings/production.py`
- Base: `backend/config/settings/base.py`

Look for:
```python
# LDAP Configuration
AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_LDAP_SERVER_URI = os.getenv('LDAP_SERVER_URI')
AUTH_LDAP_BIND_DN = os.getenv('LDAP_BIND_DN')
AUTH_LDAP_BIND_PASSWORD = os.getenv('LDAP_BIND_PASSWORD')
# ... more LDAP settings
```

### Test LDAP Connection

Use the `test_ldap` management command:

```bash
docker-compose exec backend python manage.py test_ldap <username>
```

Example:
```bash
docker-compose exec backend python manage.py test_ldap john.doe
```

Expected output (success):
```
Testing LDAP connection for user: john.doe
✓ Successfully connected to LDAP server: ldap://dc.example.local:389
✓ User found in Active Directory
✓ Distinguished Name: CN=John Doe,CN=Users,DC=example,DC=local
✓ User attributes:
  - First Name: John
  - Last Name: Doe
  - Email: john.doe@example.com
  - sAMAccountName: john.doe

LDAP test completed successfully!
```

Expected output (failure):
```
Testing LDAP connection for user: john.doe
✗ Error: Can't contact LDAP server
  Check LDAP_SERVER_URI in your .env file
  Verify the LDAP server is accessible from this container
```

### LDAP Troubleshooting

If LDAP test fails:

1. **Verify environment variables:**
   ```bash
   docker-compose exec backend env | grep LDAP
   ```

2. **Test network connectivity:**
   ```bash
   docker-compose exec backend ping dc.example.local
   docker-compose exec backend telnet dc.example.local 389
   ```

3. **Check LDAP server with ldapsearch:**
   ```bash
   docker-compose exec backend ldapsearch \
     -x -H ldap://dc.example.local:389 \
     -D "CN=Service Account,OU=ServiceAccounts,DC=example,DC=local" \
     -w "password" \
     -b "CN=Users,DC=example,DC=local" \
     "(sAMAccountName=john.doe)"
   ```

4. **Enable LDAP debug logging:**
   
   Add to Django settings:
   ```python
   import logging
   logger = logging.getLogger('django_auth_ldap')
   logger.addHandler(logging.StreamHandler())
   logger.setLevel(logging.DEBUG)
   ```
   
   Rebuild and check logs:
   ```bash
   docker-compose build backend
   docker-compose up -d
   docker-compose logs -f backend
   ```

For detailed LDAP setup instructions, see: [ldap-setup.md](ldap-setup.md)

---

## Management Commands

### Available Commands

List all available management commands:
```bash
docker-compose exec backend python manage.py help
```

### Common Commands

**Database:**
```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create migrations for model changes
docker-compose exec backend python manage.py makemigrations

# Show migration status
docker-compose exec backend python manage.py showmigrations

# Reset database (dangerous!)
docker-compose exec backend python manage.py flush
```

**Users and Roles:**
```bash
# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Initialize roles
docker-compose exec backend python manage.py init_roles

# Change user password
docker-compose exec backend python manage.py changepassword admin
```

**Testing:**
```bash
# Test LDAP connection
docker-compose exec backend python manage.py test_ldap username

# Validate project structure
docker-compose exec backend python manage.py validate_structure
```

**Development:**
```bash
# Open Django shell
docker-compose exec backend python manage.py shell

# Open database shell
docker-compose exec backend python manage.py dbshell

# Collect static files (for production)
docker-compose exec backend python manage.py collectstatic

# Run tests
docker-compose exec backend python manage.py test
```

---

## Development Workflow

### Making Code Changes

1. Edit code in your local editor (changes are synced via volume mounts)

2. Restart backend to apply changes:
   ```bash
   docker-compose restart backend
   ```

3. View logs:
   ```bash
   docker-compose logs -f backend
   ```

### Running Tests

```bash
# Run all tests
docker-compose exec backend pytest

# Run specific test file
docker-compose exec backend pytest apps/users/tests/test_models.py

# Run with coverage
docker-compose exec backend pytest --cov=apps --cov-report=html

# Run with verbose output
docker-compose exec backend pytest -v
```

### Database Management

**Create backup:**
```bash
docker-compose exec db pg_dump -U postgres project_management > backup.sql
```

**Restore backup:**
```bash
docker-compose exec -T db psql -U postgres project_management < backup.sql
```

**Access database directly:**
```bash
docker-compose exec db psql -U postgres -d project_management
```

---

## Logs and Debugging

### View Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f backend

# Last N lines
docker-compose logs --tail=100 backend

# Logs since timestamp
docker-compose logs --since 2024-01-01T10:00:00 backend
```

### Debug in Container

Get a shell in the backend container:

```bash
docker-compose exec backend bash
```

Inside the container:
```bash
# Check Python packages
pip list

# Check environment variables
env | grep DB_

# Check Django configuration
python manage.py check

# Test database connection
python manage.py dbshell

# View Django shell
python manage.py shell
```

### Common Debug Tasks

**Check if database is accessible:**
```bash
docker-compose exec backend python -c "import psycopg2; conn = psycopg2.connect('dbname=project_management user=postgres password=postgres host=db'); print('DB Connected!')"
```

**Check if Redis is accessible:**
```bash
docker-compose exec backend python -c "import redis; r = redis.from_url('redis://redis:6379/0'); r.ping(); print('Redis Connected!')"
```

**Validate Django settings:**
```bash
docker-compose exec backend python manage.py check --deploy
```

---

## Stopping and Cleaning Up

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (deletes database!)
docker-compose down -v

# Stop specific service
docker-compose stop backend
```

### Rebuild After Changes

```bash
# Rebuild specific service
docker-compose build backend

# Rebuild without cache
docker-compose build --no-cache backend

# Rebuild and start
docker-compose up -d --build
```

### Clean Up

```bash
# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Complete cleanup (be careful!)
docker system prune -a --volumes
```

---

## Production Deployment Notes

For production deployment, additional steps are required:

1. **Security:**
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure `ALLOWED_HOSTS` properly
   - Use HTTPS/SSL
   - Enable CSRF protection

2. **Database:**
   - Use production-grade PostgreSQL
   - Set up regular backups
   - Configure connection pooling

3. **Static Files:**
   ```bash
   docker-compose exec backend python manage.py collectstatic --noinput
   ```

4. **WSGI Server:**
   - Use Gunicorn or uWSGI instead of development server
   - Configure worker processes appropriately

5. **Reverse Proxy:**
   - Set up Nginx or Apache
   - Configure SSL certificates
   - Set up load balancing if needed

6. **Monitoring:**
   - Configure application logging
   - Set up error tracking (e.g., Sentry)
   - Monitor performance metrics

See backend/README.md for detailed production deployment instructions.

---

## Quick Reference

### Essential Commands

```bash
# Start everything
docker-compose up -d

# View status
docker-compose ps

# View logs
docker-compose logs -f backend

# Restart backend
docker-compose restart backend

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Test LDAP
docker-compose exec backend python manage.py test_ldap username

# Stop everything
docker-compose down
```

### URLs

- Backend API: http://localhost:8000
- Django Admin: http://localhost:8000/admin
- Swagger API Docs: http://localhost:8000/api/schema/swagger/
- ReDoc API Docs: http://localhost:8000/api/schema/redoc/

### Default Credentials

- Username: `admin`
- Password: `admin123`

⚠️ **Change these in production!**

---

## Troubleshooting

For common issues and solutions, see:
- [docker-troubleshooting.md](docker-troubleshooting.md) - Docker-related issues
- [ldap-setup.md](ldap-setup.md) - LDAP configuration and issues
- [issue-log.md](issue-log.md) - Chronological log of known issues

---

## Summary

This guide covered:
- ✅ Initial environment configuration
- ✅ Starting Docker services
- ✅ Running database migrations
- ✅ Creating roles and superuser
- ✅ Accessing the application and API
- ✅ Key API endpoints
- ✅ LDAP configuration (optional)
- ✅ Management commands
- ✅ Development workflow
- ✅ Logs and debugging
- ✅ Stopping and cleaning up

Your backend should now be running and accessible at http://localhost:8000!
