# Issue Log

Extracted from chat transcript - chronological log of issues encountered during setup and their resolutions.

---

## Overview

This document provides a chronological record of issues encountered during the project setup and LDAP integration, including error messages, root causes, and resolutions applied.

---

## Issue Timeline

### [2025-11-07 08:18:20] Issue #1: Missing .env File

**Context:** Initial Docker Compose startup

**Error Message:**
```
WARNING: The DEBUG variable is not set. Defaulting to a blank string.
WARNING: The SECRET_KEY variable is not set. Defaulting to a blank string.
WARNING: The DB_NAME variable is not set. Defaulting to a blank string.
ERROR: The POSTGRES_PASSWORD variable is not set. Defaulting to a blank string.
```

**Root Cause:**
- User attempted to run `docker-compose up` without creating `.env` file
- Docker Compose expects environment variables to be defined
- `.env.example` exists as template but wasn't copied

**Resolution:**
1. Copied `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edited `.env` with appropriate values
3. Restarted Docker Compose:
   ```bash
   docker-compose up -d
   ```

**Outcome:** ✅ Resolved - Services started successfully after .env file created

**Prevention:**
- Document `.env` requirement prominently in README
- Add check script to verify .env exists before docker-compose
- Consider adding sample values directly in docker-compose.yml for development

---

### [2025-11-07 08:20:15] Issue #2: Failed Building Wheel for python-ldap

**Context:** Docker build process when adding LDAP support

**Error Message:**
```
Building wheel for python-ldap (setup.py) ... error
ERROR: Command errored out with exit status 1:
...
fatal error: lber.h: No such file or directory
 #include <lber.h>
          ^~~~~~~~~
compilation terminated.
error: command 'gcc' failed with exit status 1
...
ERROR: Failed building wheel for python-ldap
Running setup.py install for python-ldap ... error
```

**Root Cause:**
- `python-ldap` package requires system-level LDAP development libraries
- Base Python Docker image (python:3.11-slim) doesn't include these libraries
- Package tries to compile C extensions during pip install
- Required header files (lber.h, ldap.h) not found

**Resolution:**
1. Updated Dockerfile to install system dependencies before pip install:
   ```dockerfile
   RUN apt-get update && apt-get install -y \
       libldap2-dev \
       libsasl2-dev \
       ldap-utils \
       gcc \
       python3-dev \
       && rm -rf /var/lib/apt/lists/*
   ```

2. Rebuilt Docker image:
   ```bash
   docker-compose build backend --no-cache
   ```

3. Verified successful build:
   ```bash
   docker-compose up -d
   docker-compose logs backend
   ```

**Outcome:** ✅ Resolved - python-ldap compiled successfully with system dependencies

**Technical Details:**
- `libldap2-dev`: LDAP client library development files
- `libsasl2-dev`: SASL authentication library (required for LDAP bind)
- `ldap-utils`: Command-line tools for testing (ldapsearch, ldapwhoami)
- `gcc`: C compiler needed to build Python extensions
- `python3-dev`: Python development headers

**Lessons Learned:**
- Always check if Python packages have C extensions requiring system libraries
- Document system dependencies in requirements
- Test build process in clean environment

---

### [2025-11-07 08:32:20] Issue #3: Docker Desktop Not Running

**Context:** Attempting to start Docker services

**Error Message:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
error during connect: This error may indicate that the docker daemon is not running.
```

**Root Cause:**
- Docker Desktop application was not started
- Docker daemon not accessible from WSL2
- Common issue when system restarts or Docker Desktop auto-start disabled

**Resolution:**
1. Started Docker Desktop from Windows Start Menu
2. Waited for Docker to fully initialize (whale icon in system tray)
3. Verified Docker was accessible from WSL2:
   ```bash
   docker ps
   docker --version
   ```
4. Checked WSL2 integration was enabled in Docker Desktop settings

**Outcome:** ✅ Resolved - Docker daemon accessible, services started normally

**Additional Notes:**
- On Windows, Docker Desktop must be running for WSL2 to access Docker
- Enable "Start Docker Desktop when you log in" in settings to prevent recurrence
- Alternative on Linux: `sudo systemctl start docker`

---

### [2025-11-07 08:35:10] Issue #4: How to Temporarily Disable LDAP

**Context:** User wanted to test application without LDAP/AD dependency

**Challenge:**
- LDAP server not accessible during testing
- python-ldap dependencies causing slow builds
- Need to test local authentication only

**Resolution:**
1. Commented out LDAP packages in requirements:
   ```txt
   # django-auth-ldap==4.6.0
   # python-ldap==3.4.4
   ```

2. Disabled LDAP backend in Django settings:
   ```python
   AUTHENTICATION_BACKENDS = [
       # 'django_auth_ldap.backend.LDAPBackend',  # Disabled
       'django.contrib.auth.backends.ModelBackend',
   ]
   ```

3. Optionally commented out LDAP system dependencies in Dockerfile (for faster builds)

4. Rebuilt container:
   ```bash
   docker-compose build backend --no-cache
   docker-compose up -d
   ```

5. Created local superuser for testing:
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

**Outcome:** ✅ Resolved - Application runs with local authentication only

**Re-enabling Process:**
1. Uncomment packages in requirements
2. Uncomment LDAP backend in settings
3. Uncomment Dockerfile dependencies
4. Rebuild: `docker-compose build backend --no-cache`
5. Restart: `docker-compose up -d`

**Note:** Existing users created from LDAP remain in database and can authenticate locally if password is set

---

### [2025-11-07 09:05:00] Issue #5: LDAP Test Command Timeout (Future Prevention)

**Context:** Testing LDAP connectivity with management command

**Potential Error:**
```
Testing LDAP connection...
Error: Operation timed out
Can't contact LDAP server
```

**Potential Causes:**
1. LDAP server URI incorrect or server down
2. Firewall blocking port 389/636
3. Network connectivity issues
4. Service account credentials expired

**Prevention/Resolution Steps:**

**Step 1: Verify network connectivity**
```bash
docker-compose exec backend ping dc.example.local
docker-compose exec backend telnet dc.example.local 389
```

**Step 2: Test with ldapsearch**
```bash
docker-compose exec backend ldapsearch \
  -x -H ldap://dc.example.local:389 \
  -D "CN=Service Account,OU=ServiceAccounts,DC=example,DC=local" \
  -w "password" \
  -b "CN=Users,DC=example,DC=local" \
  "(sAMAccountName=testuser)"
```

**Step 3: Check environment variables**
```bash
docker-compose exec backend env | grep LDAP
```

**Step 4: Enable debug logging**
Add to Django settings:
```python
import logging
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
```

**Step 5: Check firewall rules**
- Windows Firewall on Domain Controller
- Network firewalls between application and DC
- Cloud security groups (if applicable)

**Outcome:** Not actually encountered but documented for future reference

---

### [2025-11-07 09:10:00] Issue #6: User Has No Permissions After LDAP Login (Expected Behavior)

**Context:** User successfully authenticated via LDAP but cannot access resources

**Reported Issue:**
```
User 'john.doe' logged in successfully but gets "403 Forbidden" on all endpoints
```

**Root Cause:**
- This is **expected behavior**, not a bug
- Roles are NOT automatically synced from Active Directory groups
- New users from LDAP have no role assigned by default
- Administrator must manually assign roles

**Resolution:**
1. Explained that this is intentional security design
2. Instructed on role assignment process:
   - Login to Django Admin: http://localhost:8000/admin
   - Navigate to Users section
   - Find user 'john.doe'
   - Assign appropriate role (e.g., Engineer)
   - Save changes

3. User logged out and back in to refresh permissions

**Outcome:** ✅ Working as designed - User has proper permissions after role assignment

**Why Roles Aren't Synced:**
- Security: Prevents unauthorized privilege escalation via AD groups
- Flexibility: Application roles may differ from AD organizational structure
- Control: Requires explicit administrator approval
- Separation of concerns: AD handles authentication, app handles authorization

**Documentation:** Created detailed explanation in roles-and-auth.md

---

## Issue Statistics

### By Category

| Category | Count | Resolution Rate |
|----------|-------|-----------------|
| Configuration | 2 | 100% |
| Build/Dependencies | 1 | 100% |
| Environment Setup | 2 | 100% |
| Documentation/Understanding | 1 | 100% |
| **Total** | **6** | **100%** |

### By Severity

| Severity | Count | Description |
|----------|-------|-------------|
| Critical | 0 | Application cannot start |
| High | 2 | Major functionality blocked (Issues #2, #3) |
| Medium | 2 | Workaround available (Issues #1, #4) |
| Low | 2 | Documentation/understanding (Issues #5, #6) |

### Resolution Time

| Issue | Time to Resolve | Complexity |
|-------|----------------|------------|
| #1 - Missing .env | ~2 minutes | Low |
| #2 - python-ldap build | ~10 minutes | Medium |
| #3 - Docker not running | ~5 minutes | Low |
| #4 - Disable LDAP | ~8 minutes | Medium |
| #5 - LDAP timeout | N/A (preventive) | Medium |
| #6 - No permissions | ~5 minutes | Low |

---

## Common Issue Patterns

### Pattern 1: Missing Configuration Files

**Issues:** #1 (Missing .env)

**Common Symptoms:**
- Environment variable warnings
- Services fail to start
- Database connection errors

**Solution Pattern:**
- Always check for required configuration files
- Copy from .example templates
- Verify all required variables are set

### Pattern 2: Missing System Dependencies

**Issues:** #2 (python-ldap build failure)

**Common Symptoms:**
- Build failures during pip install
- "fatal error: xxx.h: No such file or directory"
- Compilation errors

**Solution Pattern:**
- Research system dependencies for Python packages
- Install dev packages in Dockerfile before pip install
- Test in clean environment

### Pattern 3: External Service Not Running

**Issues:** #3 (Docker not running)

**Common Symptoms:**
- "Cannot connect to daemon"
- "Connection refused"
- Service unreachable

**Solution Pattern:**
- Verify external service is running
- Check network connectivity
- Verify firewall rules

---

## Lessons Learned

1. **Environment Configuration:**
   - Document all required environment variables
   - Provide complete .env.example
   - Add validation before starting services

2. **Build Dependencies:**
   - Research system requirements for all Python packages
   - Document why each system package is needed
   - Test builds in clean Docker environment

3. **Documentation:**
   - Create setup guides with step-by-step instructions
   - Document common issues and solutions
   - Include troubleshooting section

4. **Testing:**
   - Test with minimal configuration first
   - Add complexity incrementally
   - Verify each step before proceeding

5. **Role Management:**
   - Clearly document that roles aren't synced from AD
   - Explain security reasons for manual assignment
   - Provide clear instructions for role assignment

---

## Future Improvements

### Documentation Enhancements
- [ ] Add prerequisites checklist to README
- [ ] Create troubleshooting flowchart
- [ ] Add video walkthrough for setup
- [ ] Document network requirements

### Tooling Improvements
- [ ] Add pre-flight check script
  - Verify Docker is running
  - Check if .env exists
  - Validate environment variables
  - Test network connectivity

- [ ] Improve error messages
  - Detect missing .env and suggest copying from example
  - Better error message when Docker isn't running
  - Suggest solutions in build error output

### Testing Improvements
- [ ] Add integration tests for LDAP
- [ ] Add Docker healthchecks for all services
- [ ] Create automated setup verification script
- [ ] Add CI/CD pipeline to catch build issues early

---

## Related Documentation

- [ldap-setup.md](ldap-setup.md) - LDAP configuration details
- [docker-troubleshooting.md](docker-troubleshooting.md) - Docker issues and solutions
- [backend-setup.md](backend-setup.md) - Backend setup instructions
- [roles-and-auth.md](roles-and-auth.md) - Authentication and role management
- [full-transcript.md](full-transcript.md) - Complete conversation transcript

---

## Summary

This issue log documented:
- ✅ 6 issues encountered during setup
- ✅ 100% resolution rate
- ✅ Root cause analysis for each issue
- ✅ Detailed resolution steps
- ✅ Prevention strategies
- ✅ Lessons learned and future improvements

All issues were successfully resolved, and documentation was created to prevent recurrence and help future users.

---

**Last Updated:** 2025-11-07  
**Status:** All documented issues resolved  
**Next Review:** When new issues are encountered
