# Quick Start Guide

Get your Project Management Platform up and running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- Git installed

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Crack8502pl/project-management-platform.git
cd project-management-platform
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

The default values in `.env.example` are suitable for development. For production, make sure to:
- Set `DEBUG=False`
- Change `SECRET_KEY` to a secure random string
- Update database credentials
- Configure email settings

### 3. Start the Services

```bash
docker-compose up -d
```

This command will:
- Start PostgreSQL database
- Start Redis for Celery
- Build and start the Django backend
- Start Celery worker for background tasks
- Start Celery beat for scheduled tasks

### 4. Wait for Services to Start

Monitor the logs to ensure all services are running:

```bash
docker-compose logs -f backend
```

Wait until you see:
```
Starting server...
```

Press `Ctrl+C` to exit logs.

### 5. Access the Platform

The backend is now running! You can access:

- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
  - Username: `admin`
  - Password: `admin123`
- **API Documentation**:
  - Swagger UI: http://localhost:8000/api/schema/swagger/
  - ReDoc: http://localhost:8000/api/schema/redoc/

## Quick Test

### Test API Authentication

```bash
# Obtain JWT token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# You should receive a response with access and refresh tokens
# Copy the access token for the next request

# Get current user info
curl http://localhost:8000/api/auth/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Test with Swagger UI

1. Open http://localhost:8000/api/schema/swagger/
2. Click "Authorize" button at the top
3. Use credentials: `admin` / `admin123`
4. Try different API endpoints!

## Next Steps

### Create Additional Users

1. Go to http://localhost:8000/admin/
2. Login with admin credentials
3. Navigate to "Authentication" > "Users"
4. Click "Add User"
5. Assign appropriate role

### Create Your First Project

Using the API or admin panel:

1. Go to "Projects" > "Projects"
2. Click "Add Project"
3. Fill in:
   - Name: e.g., "Railway Station Network"
   - Code: e.g., "RSN-001"
   - Status: "Planning"
   - Manager: Select a user

### Create Tasks

1. Go to "Tasks" > "Tasks"
2. Create a task with:
   - Project: Select your project
   - Title: e.g., "Install SMW cameras"
   - Task Type: "SMW"
   - Status: "To Do"

## Stopping the Services

```bash
docker-compose down
```

To stop and remove all data (including database):
```bash
docker-compose down -v
```

## Troubleshooting

### Services Won't Start

Check logs for specific service:
```bash
docker-compose logs backend
docker-compose logs db
docker-compose logs redis
```

### Database Connection Issues

Ensure PostgreSQL is healthy:
```bash
docker-compose ps
```

All services should show "healthy" status.

### Reset Everything

```bash
docker-compose down -v
docker-compose up -d
```

## Common Commands

```bash
# View logs
docker-compose logs -f

# Restart a service
docker-compose restart backend

# Run Django commands
docker-compose exec backend python manage.py <command>

# Create migrations
docker-compose exec backend python manage.py makemigrations

# Access Django shell
docker-compose exec backend python manage.py shell

# Access database shell
docker-compose exec db psql -U postgres -d project_management
```

## Development Mode

For active development with code changes:

```bash
# Backend automatically reloads on code changes
docker-compose up

# Run migrations after model changes
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

## Production Deployment

See [backend/README.md](backend/README.md) for detailed production deployment instructions.

## Getting Help

- Check [README.md](README.md) for detailed information
- Review API documentation at http://localhost:8000/api/schema/swagger/
- Check backend documentation at [backend/README.md](backend/README.md)

## Security Notes

⚠️ **Important**: The default credentials are for development only!

For production:
1. Change all default passwords
2. Use strong SECRET_KEY
3. Enable HTTPS
4. Configure proper firewall rules
5. Set DEBUG=False
6. Use environment-specific settings

Happy coding! 🚀
