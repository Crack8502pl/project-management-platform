# Docker and Docker Compose Troubleshooting

Extracted from chat transcript - common Docker issues and their solutions.

---

## Overview

This document compiles Docker and docker-compose related issues encountered during project setup, along with their solutions and prevention tips.

---

## Common Issues and Solutions

### Issue 1: Missing .env File

**Error Message:**
```
WARNING: The DEBUG variable is not set. Defaulting to a blank string.
WARNING: The SECRET_KEY variable is not set. Defaulting to a blank string.
ERROR: The POSTGRES_PASSWORD variable is not set.
```

**Cause:**
Docker Compose expects environment variables to be set, typically from a `.env` file in the same directory as `docker-compose.yml`.

**Solution:**
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your actual values:
   ```bash
   nano .env  # or use your preferred editor
   ```

3. Verify the file exists:
   ```bash
   ls -la .env
   cat .env  # Check contents (be careful with sensitive data)
   ```

4. Restart Docker Compose:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

**Prevention:**
- Always keep `.env.example` up-to-date as a template
- Add `.env` to `.gitignore` (should already be there)
- Document required environment variables in README
- Consider using `.env.local` for local development overrides

---

### Issue 2: Docker Desktop Not Running

**Error Message:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```
or
```
error during connect: This error may indicate that the docker daemon is not running.
```

**Cause:**
Docker Desktop application is not running, or Docker daemon is not started.

**Solutions by Platform:**

#### Windows with WSL2:
1. Start Docker Desktop application from Start Menu
2. Wait for Docker Desktop to fully start (check system tray icon)
3. Verify WSL2 integration is enabled:
   - Open Docker Desktop settings
   - Go to Resources → WSL Integration
   - Ensure your WSL2 distribution is enabled
4. In WSL2, verify Docker is accessible:
   ```bash
   docker ps
   docker --version
   ```

#### Linux:
1. Start Docker daemon:
   ```bash
   sudo systemctl start docker
   ```

2. Enable Docker to start on boot:
   ```bash
   sudo systemctl enable docker
   ```

3. Verify Docker is running:
   ```bash
   systemctl status docker
   docker ps
   ```

4. Add your user to docker group (to avoid using sudo):
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker  # or logout and login again
   ```

#### macOS:
1. Start Docker Desktop from Applications
2. Wait for the whale icon to appear in the menu bar and stop animating
3. Verify:
   ```bash
   docker ps
   ```

**Prevention:**
- Set Docker Desktop to start automatically on system startup
- Add a quick check to your setup scripts:
  ```bash
  if ! docker info > /dev/null 2>&1; then
      echo "Docker is not running. Please start Docker Desktop."
      exit 1
  fi
  ```

---

### Issue 3: Failed Building Wheel for python-ldap

**Error Message:**
```
Building wheel for python-ldap (setup.py) ... error
ERROR: Command errored out with exit status 1:
...
fatal error: lber.h: No such file or directory
...
ERROR: Failed building wheel for python-ldap
```

**Cause:**
The `python-ldap` package requires system-level LDAP libraries to compile. These are not present in the base Python Docker image.

**Solution:**

1. **Update Dockerfile** - Add system dependencies before pip install:

   ```dockerfile
   FROM python:3.11-slim

   # Install system dependencies for python-ldap
   RUN apt-get update && apt-get install -y \
       libldap2-dev \
       libsasl2-dev \
       ldap-utils \
       gcc \
       python3-dev \
       && rm -rf /var/lib/apt/lists/*

   # Now install Python packages
   COPY requirements /requirements
   RUN pip install --no-cache-dir -r /requirements/production.txt
   ```

   **Required packages explained:**
   - `libldap2-dev` - LDAP client library development files
   - `libsasl2-dev` - SASL authentication library development files
   - `ldap-utils` - LDAP command-line utilities (useful for debugging)
   - `gcc` - Compiler needed to build Python extensions
   - `python3-dev` - Python development headers

2. **Rebuild the Docker image:**
   ```bash
   docker-compose build backend --no-cache
   ```

3. **Start the services:**
   ```bash
   docker-compose up -d
   ```

**Alternative Solution - Use Alpine Linux:**

If using Alpine-based images, use these packages instead:

```dockerfile
FROM python:3.11-alpine

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    openldap-dev \
    libffi-dev
```

**Prevention:**
- Document LDAP requirements in README
- Include these dependencies in Dockerfile from the start
- Consider using pre-built wheels if available

---

### Issue 4: How to Disable LDAP When Not Needed

**Scenario:**
You want to test the application without LDAP, or your environment doesn't have access to Active Directory.

**Solution:**

**Step 1: Remove/Comment LDAP Packages**

Edit `requirements/base.txt` or `requirements.txt`:

```txt
# Temporarily disabled - uncomment when LDAP is available
# django-auth-ldap==4.6.0
# python-ldap==3.4.4
```

**Step 2: Disable LDAP in Django Settings**

Edit your settings file (e.g., `config/settings/base.py`):

```python
# Authentication Backends
AUTHENTICATION_BACKENDS = [
    # Temporarily disabled - uncomment when LDAP is configured
    # 'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',  # Use local database only
]

# Comment out all LDAP-related settings
# AUTH_LDAP_SERVER_URI = os.getenv('LDAP_SERVER_URI')
# AUTH_LDAP_BIND_DN = os.getenv('LDAP_BIND_DN')
# ... etc
```

**Step 3: Remove LDAP System Dependencies from Dockerfile** (Optional)

If you want faster builds without LDAP:

```dockerfile
# Comment out LDAP dependencies
# RUN apt-get update && apt-get install -y \
#     libldap2-dev \
#     libsasl2-dev \
#     ldap-utils \
#     && rm -rf /var/lib/apt/lists/*
```

**Step 4: Rebuild and Restart**

```bash
docker-compose down
docker-compose build backend --no-cache
docker-compose up -d
```

**Step 5: Verify Local Authentication Works**

```bash
# Create a local user
docker-compose exec backend python manage.py createsuperuser

# Test login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'
```

**To Re-enable LDAP Later:**
1. Uncomment packages in requirements
2. Uncomment LDAP backend in settings
3. Uncomment Dockerfile dependencies if removed
4. Rebuild: `docker-compose build backend --no-cache`
5. Restart: `docker-compose up -d`

---

### Issue 5: Port Already in Use

**Error Message:**
```
ERROR: for backend  Cannot start service backend: driver failed programming external connectivity
Bind for 0.0.0.0:8000 failed: port is already allocated
```

**Cause:**
Another process is using the port that Docker wants to bind to.

**Solutions:**

**Option 1: Find and stop the process using the port**

On Linux/macOS:
```bash
# Find process using port 8000
sudo lsof -i :8000
# or
sudo netstat -tulpn | grep :8000

# Kill the process
sudo kill -9 <PID>
```

On Windows:
```cmd
# Find process
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

**Option 2: Change the port in docker-compose.yml**

Edit `docker-compose.yml`:
```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Changed from 8000:8000
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

Access the backend at http://localhost:8001 instead.

---

### Issue 6: Container Keeps Restarting

**Symptoms:**
```bash
$ docker-compose ps
NAME                COMMAND                  STATUS
backend             "python manage.py ru…"   Restarting
```

**Diagnosis:**

Check container logs:
```bash
docker-compose logs backend
# or for real-time logs
docker-compose logs -f backend
```

**Common Causes and Solutions:**

**Cause 1: Database not ready**
```
django.db.utils.OperationalError: could not connect to server: Connection refused
```

Solution: Add `depends_on` and health checks in docker-compose.yml:
```yaml
services:
  backend:
    depends_on:
      db:
        condition: service_healthy
    
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
```

**Cause 2: Missing environment variables**

Solution: Ensure all required variables are in `.env`

**Cause 3: Syntax error in code**

Solution: Check logs for Python tracebacks, fix the error, rebuild

**Cause 4: Wrong command or entrypoint**

Solution: Verify the command in docker-compose.yml or Dockerfile

---

### Issue 7: Volume Mount Issues on Windows

**Symptoms:**
- File changes not reflected in container
- Permission denied errors
- Slow performance

**Solutions:**

**Option 1: Enable WSL2 backend** (Recommended)
1. Use WSL2 backend in Docker Desktop (not Hyper-V)
2. Clone repository in WSL2 filesystem (not /mnt/c/)
   ```bash
   # Clone in WSL2 home directory
   cd ~
   git clone <repo-url>
   ```

**Option 2: Fix line endings**

Windows line endings (CRLF) can cause issues with Linux containers:

1. Configure git:
   ```bash
   git config --global core.autocrlf input
   ```

2. Re-clone repository or fix existing:
   ```bash
   # Fix line endings in existing files
   dos2unix entrypoint.sh  # if dos2unix is installed
   # or
   sed -i 's/\r$//' entrypoint.sh
   ```

**Option 3: Make scripts executable**

```bash
# In WSL2 or in Docker container
chmod +x entrypoint.sh
```

---

### Issue 8: Out of Disk Space

**Error Messages:**
```
no space left on device
ERROR: Service 'backend' failed to build: write /var/lib/docker/...: no space left on device
```

**Solutions:**

**Clean up Docker resources:**

```bash
# Remove stopped containers
docker container prune -f

# Remove unused images
docker image prune -a -f

# Remove unused volumes
docker volume prune -f

# Remove unused networks
docker network prune -f

# Nuclear option - clean everything (be careful!)
docker system prune -a --volumes -f
```

**Check disk usage:**
```bash
# Docker disk usage
docker system df

# System disk usage
df -h
```

**Increase Docker Desktop disk space** (if on Mac/Windows):
1. Open Docker Desktop settings
2. Go to Resources → Advanced
3. Increase "Disk image size"
4. Click Apply & Restart

---

### Issue 9: Build Context is Too Large

**Error Message:**
```
Sending build context to Docker daemon   1.5GB
```

**Cause:**
Docker is including files that shouldn't be in the build context (node_modules, .git, etc.)

**Solution:**

Create or update `.dockerignore` file in the directory with your Dockerfile:

```
# .dockerignore
.git
.gitignore
.env
.env.local
node_modules
npm-debug.log
venv
*.pyc
__pycache__
*.pyo
*.pyd
.pytest_cache
.coverage
htmlcov
dist
build
*.egg-info
.vscode
.idea
*.swp
*.swo
*~
.DS_Store
Thumbs.db
```

Then rebuild:
```bash
docker-compose build --no-cache
```

---

### Issue 10: Container Can't Connect to Other Services

**Error Message:**
```
django.db.utils.OperationalError: could not translate host name "db" to address
```

**Cause:**
Services can't resolve each other's hostnames, usually a network issue.

**Solutions:**

**Ensure services are on the same network:**

```yaml
services:
  backend:
    networks:
      - app-network
  
  db:
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

**Use correct hostnames:**
- Use service names as hostnames (e.g., `db`, not `localhost`)
- In `.env`: `DB_HOST=db` (not `localhost`)

**Restart with recreate:**
```bash
docker-compose down
docker-compose up -d --force-recreate
```

---

## WSL2-Specific Notes

### Best Practices for WSL2

1. **Clone repositories in WSL2 filesystem:**
   ```bash
   # Good - fast
   cd ~/projects
   git clone <repo>
   
   # Bad - slow
   cd /mnt/c/Users/YourName/projects
   git clone <repo>
   ```

2. **Access Docker from WSL2:**
   - Docker Desktop must have WSL2 integration enabled
   - Use `docker` commands directly in WSL2 terminal
   - No need for special configuration

3. **Memory and CPU limits:**
   - Create `.wslconfig` in Windows user home directory:
     ```ini
     [wsl2]
     memory=8GB
     processors=4
     ```
   - Restart WSL2: `wsl --shutdown` (in PowerShell)

4. **File permissions:**
   - Files created in WSL2 have correct permissions automatically
   - No need to chmod files in WSL2 filesystem

---

## Docker Compose Commands Reference

### Essential Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f [service-name]

# Build/rebuild services
docker-compose build [service-name]
docker-compose build --no-cache  # Force complete rebuild

# Restart services
docker-compose restart [service-name]

# Execute command in container
docker-compose exec backend python manage.py migrate
docker-compose exec backend bash  # Get shell access

# View running services
docker-compose ps

# View service status and health
docker-compose ps -a

# Scale services
docker-compose up -d --scale worker=3

# Pull latest images
docker-compose pull

# Remove volumes when stopping
docker-compose down -v
```

### Debugging Commands

```bash
# View logs for specific service
docker-compose logs backend

# Follow logs real-time
docker-compose logs -f backend

# View last N lines
docker-compose logs --tail=100 backend

# Check service health
docker-compose ps
docker inspect <container-id>

# Get shell in running container
docker-compose exec backend bash

# Run one-off command
docker-compose run --rm backend python manage.py shell
```

---

## Prevention Checklist

Before running `docker-compose up`, verify:

- [ ] `.env` file exists and is properly configured
- [ ] Docker Desktop is running (if on Windows/Mac)
- [ ] Ports are not already in use
- [ ] Sufficient disk space available
- [ ] `.dockerignore` is configured to exclude large directories
- [ ] All required system dependencies are in Dockerfile
- [ ] WSL2 integration enabled (if on Windows)
- [ ] Repository cloned in WSL2 filesystem (if using WSL2)

---

## Getting Help

If you encounter an issue not covered here:

1. **Check logs:**
   ```bash
   docker-compose logs backend
   ```

2. **Verify container status:**
   ```bash
   docker-compose ps
   ```

3. **Check Docker system:**
   ```bash
   docker system df
   docker info
   ```

4. **Test connectivity:**
   ```bash
   docker-compose exec backend ping db
   docker-compose exec backend curl http://redis:6379
   ```

5. **Recreate everything:**
   ```bash
   docker-compose down -v
   docker-compose build --no-cache
   docker-compose up -d
   ```

---

## Summary

This guide covered:
- ✅ Missing .env file → Copy from .env.example
- ✅ Docker Desktop not running → Start Docker Desktop, check WSL2 integration
- ✅ Failed building python-ldap → Add system dependencies to Dockerfile
- ✅ Disabling LDAP → Comment out packages and settings
- ✅ Port conflicts → Change ports or stop conflicting processes
- ✅ Container restart loops → Check logs, fix dependencies and environment
- ✅ WSL2 issues → Use WSL2 filesystem, configure integration
- ✅ Disk space → Clean up Docker resources
- ✅ Large build context → Create/update .dockerignore
- ✅ Network issues → Use service names, check networks

For additional help, refer to the full-transcript.md or Docker documentation.
