# LDAP/Active Directory Setup Guide

Extracted from chat transcript - comprehensive guide for LDAP integration with Django.

---

## Overview

This guide covers the complete setup of LDAP/Active Directory authentication for the Django project management platform. The implementation uses `django-auth-ldap` with a fallback to local database authentication.

## Prerequisites

- Active Directory Domain Controller accessible from your application
- Service account with read permissions in AD
- LDAP port (389) or LDAPS port (636) accessible
- Docker and Docker Compose installed

---

## Step 1: Install Required Packages

### Update Requirements File

Add these packages to your `requirements/base.txt` or `requirements.txt`:

```txt
django-auth-ldap==4.6.0
python-ldap==3.4.4
```

### Update Dockerfile

The `python-ldap` package requires system libraries. Add these to your Dockerfile **before** the pip install command:

```dockerfile
# Install system dependencies for python-ldap
RUN apt-get update && apt-get install -y \
    libldap2-dev \
    libsasl2-dev \
    ldap-utils \
    && rm -rf /var/lib/apt/lists/*
```

**Note:** Without these packages, you'll get "Failed building wheel for python-ldap" error.

---

## Step 2: Configure Environment Variables

### Minimal Required .env Entries

Add these to your `.env` file (copy from `.env.example` first if needed):

```env
# LDAP/Active Directory Configuration
LDAP_SERVER_URI=ldap://dc.example.local:389
LDAP_BIND_DN=CN=Service Account,OU=ServiceAccounts,DC=example,DC=local
LDAP_BIND_PASSWORD=[REDACTED]
LDAP_USER_SEARCH_BASE=CN=Users,DC=example,DC=local
```

### Configuration Details

- **LDAP_SERVER_URI**: 
  - Format: `ldap://hostname:port` or `ldaps://hostname:port`
  - Example: `ldap://dc.example.local:389`
  - Use `ldaps://` for SSL/TLS (port 636)

- **LDAP_BIND_DN**: 
  - Distinguished Name of service account
  - Example: `CN=SVC_DjangoLDAP,OU=ServiceAccounts,DC=example,DC=local`
  - Must have read permissions to query users

- **LDAP_BIND_PASSWORD**: 
  - Password for the service account
  - Keep this secure, never commit to version control
  - Use strong, randomly generated password

- **LDAP_USER_SEARCH_BASE**: 
  - Base DN where users are located
  - Example: `CN=Users,DC=example,DC=local`
  - Can be more specific: `OU=Employees,DC=example,DC=local`

---

## Step 3: Django Settings Configuration

Add or update the following in your Django settings file (e.g., `config/settings/base.py`):

```python
import os
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',  # Try LDAP first
    'django.contrib.auth.backends.ModelBackend',  # Fallback to local DB
]

# LDAP Configuration
AUTH_LDAP_SERVER_URI = os.getenv('LDAP_SERVER_URI')
AUTH_LDAP_BIND_DN = os.getenv('LDAP_BIND_DN')
AUTH_LDAP_BIND_PASSWORD = os.getenv('LDAP_BIND_PASSWORD')

# User Search
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    os.getenv('LDAP_USER_SEARCH_BASE', 'CN=Users,DC=example,DC=local'),
    ldap.SCOPE_SUBTREE,
    "(sAMAccountName=%(user)s)"
)

# Map AD attributes to Django user fields
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

# Create local user on first login
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Optional: Group settings (if you want to map AD groups to Django groups)
# AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
#     "OU=Groups,DC=example,DC=local",
#     ldap.SCOPE_SUBTREE,
#     "(objectClass=group)"
# )
# AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

# Optional: Logging for debugging
import logging
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
```

---

## Step 4: Active Directory Setup

### Create Service Account (PowerShell)

Run this PowerShell script on your Domain Controller or a machine with AD PowerShell module:

```powershell
# Create LDAP Service Account for Django Application
# Run with appropriate domain admin privileges

# Variables - CUSTOMIZE THESE
$ServiceAccountName = "SVC_DjangoLDAP"
$ServiceAccountPassword = ConvertTo-SecureString "[REDACTED]" -AsPlainText -Force
$ServiceAccountOU = "OU=ServiceAccounts,DC=example,DC=local"
$Description = "Service account for Django LDAP authentication"

# Create the service account
New-ADUser `
    -Name $ServiceAccountName `
    -SamAccountName $ServiceAccountName `
    -UserPrincipalName "$ServiceAccountName@example.local" `
    -Path $ServiceAccountOU `
    -AccountPassword $ServiceAccountPassword `
    -Description $Description `
    -Enabled $true `
    -PasswordNeverExpires $true `
    -CannotChangePassword $true

Write-Host "Service account created successfully"
Write-Host "DN: CN=$ServiceAccountName,$ServiceAccountOU"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Ensure account has read permissions to user search base"
Write-Host "2. Add credentials to .env file"
Write-Host "3. Test LDAP connection"
```

### Verify Service Account Permissions

The service account needs:
- Read permission on user objects in the search base
- Read permission on user attributes: givenName, sn, mail, sAMAccountName
- No special group memberships required (read-only access)

### Test LDAP Connectivity from Application Server

Use `ldapsearch` command to verify connectivity:

```bash
ldapsearch -x -H ldap://dc.example.local:389 \
  -D "CN=SVC_DjangoLDAP,OU=ServiceAccounts,DC=example,DC=local" \
  -w "password" \
  -b "CN=Users,DC=example,DC=local" \
  "(sAMAccountName=testuser)"
```

---

## Step 5: Docker Compose Configuration

### Example docker-compose.yml snippet

```yaml
services:
  backend:
    build: ./backend
    environment:
      - DEBUG=${DEBUG}
      - LDAP_SERVER_URI=${LDAP_SERVER_URI}
      - LDAP_BIND_DN=${LDAP_BIND_DN}
      - LDAP_BIND_PASSWORD=${LDAP_BIND_PASSWORD}
      - LDAP_USER_SEARCH_BASE=${LDAP_USER_SEARCH_BASE}
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
```

Make sure your `.env` file is in the same directory as `docker-compose.yml` or explicitly reference it:

```bash
docker-compose --env-file .env up -d
```

---

## Step 6: Testing LDAP Integration

### Test LDAP Connection with Management Command

Create or use the `test_ldap` management command:

```bash
# Test LDAP connection and user search
docker-compose exec backend python manage.py test_ldap username

# Example output:
# Testing LDAP connection for user: username
# ✓ Successfully connected to LDAP server
# ✓ User found in Active Directory
# ✓ User attributes: {'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@example.com'}
```

### Test Login via API

```bash
# Test login with LDAP credentials
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "[REDACTED]"}'

# Expected response:
# {
#   "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "user": {
#     "id": 1,
#     "username": "testuser",
#     "email": "testuser@example.com",
#     "first_name": "Test",
#     "last_name": "User"
#   }
# }
```

### Verify User Created in Django Admin

1. Login to Django Admin: http://localhost:8000/admin
2. Navigate to Users section
3. Find the user that logged in via LDAP
4. Verify that first_name, last_name, and email were populated from AD

---

## Step 7: How to Enable/Disable LDAP

### To Enable LDAP:

1. Ensure packages are in requirements:
   ```txt
   django-auth-ldap==4.6.0
   python-ldap==3.4.4
   ```

2. Ensure LDAP backend is in settings:
   ```python
   AUTHENTICATION_BACKENDS = [
       'django_auth_ldap.backend.LDAPBackend',
       'django.contrib.auth.backends.ModelBackend',
   ]
   ```

3. Set environment variables in `.env`

4. Rebuild and restart:
   ```bash
   docker-compose build backend
   docker-compose up -d
   ```

### To Disable LDAP:

1. Comment out packages in requirements:
   ```txt
   # django-auth-ldap==4.6.0
   # python-ldap==3.4.4
   ```

2. Remove or comment out LDAP backend:
   ```python
   AUTHENTICATION_BACKENDS = [
       # 'django_auth_ldap.backend.LDAPBackend',  # Disabled
       'django.contrib.auth.backends.ModelBackend',
   ]
   ```

3. Rebuild and restart:
   ```bash
   docker-compose build backend
   docker-compose up -d
   ```

**Note:** Disabling LDAP won't affect existing users created from AD. They remain in the local database and can still authenticate if you set a local password.

---

## Troubleshooting

### Issue: "Failed building wheel for python-ldap"

**Cause:** Missing system dependencies for compiling python-ldap

**Solution:** Add to Dockerfile before pip install:
```dockerfile
RUN apt-get update && apt-get install -y \
    libldap2-dev \
    libsasl2-dev \
    ldap-utils \
    && rm -rf /var/lib/apt/lists/*
```

### Issue: "Can't contact LDAP server"

**Possible causes and solutions:**

1. LDAP server URI incorrect
   - Verify with: `ping dc.example.local`
   - Check port: `telnet dc.example.local 389`

2. Firewall blocking LDAP port
   - Ensure port 389 (or 636 for LDAPS) is open
   - Check Windows Firewall on DC
   - Check network firewalls

3. Service account credentials incorrect
   - Verify DN format is correct
   - Test with ldapsearch command
   - Check password hasn't expired

### Issue: "Invalid credentials" when user tries to login

**Possible causes:**

1. User doesn't exist in AD
   - Verify user exists in specified search base
   - Check sAMAccountName matches username

2. User password incorrect
   - Test AD password separately
   - Check for account lockouts in AD

3. Search base is incorrect
   - Verify user is under specified LDAP_USER_SEARCH_BASE
   - Try broader search base (e.g., DC=example,DC=local)

### Issue: User logs in but has no first name/last name/email

**Cause:** AD attributes not mapped or not present

**Solution:**
1. Verify attributes exist in AD for the user
2. Check AUTH_LDAP_USER_ATTR_MAP in settings
3. Enable debug logging to see which attributes are returned

### Issue: LDAP works but users have no permissions

**This is expected behavior!** Roles are not synced from AD.

**Solution:** Assign roles manually in Django Admin:
1. Go to http://localhost:8000/admin
2. Navigate to Users
3. Edit the user
4. Assign appropriate role from dropdown
5. Save

---

## Authentication Flow

Understanding the authentication flow helps with troubleshooting:

```
1. User submits username/password to /api/auth/login/
   ↓
2. Django checks AUTHENTICATION_BACKENDS in order
   ↓
3. LDAPBackend tries to authenticate:
   a. Binds to LDAP server with service account
   b. Searches for user by sAMAccountName
   c. If found, attempts to bind as that user with provided password
   d. If successful, creates/updates local Django user
   e. Returns user object
   ↓
4. If LDAPBackend fails, ModelBackend checks local database
   ↓
5. If authentication succeeds, JWT tokens are generated and returned
   ↓
6. User can now access API with JWT token
```

---

## Role Assignment Process

**Important:** Roles are NOT automatically synced from Active Directory groups.

### Why Not Sync Roles?

1. **Security:** Prevents unauthorized role escalation via AD group membership
2. **Flexibility:** Different role models in Django vs AD
3. **Control:** Explicit administrator approval required for role assignment

### How to Assign Roles

**After user first logs in via LDAP:**

1. User account is created in Django with AD attributes
2. User has no role assigned (or default role if configured)
3. Administrator must manually assign role:
   - Login to Django Admin: http://localhost:8000/admin
   - Go to Users section
   - Find the user
   - Click to edit
   - Select role from the "Role" dropdown
   - Click Save

**Available Roles:**
- Administrator - Full system access and configuration
- Manager - Project management and team coordination  
- Engineer - Technical task management and device configuration
- Technician - Field work and checklist management
- Viewer - Read-only access to projects and documentation

---

## Security Best Practices

1. **Use LDAPS (SSL/TLS):** Use `ldaps://` instead of `ldap://` when possible
2. **Strong Service Account Password:** Generate random, long password
3. **Least Privilege:** Service account should only have read permissions
4. **Secure .env File:** Never commit .env to version control
5. **Password Expiration:** Consider if service account password should never expire
6. **Monitor Access:** Log LDAP authentication attempts
7. **Network Security:** Restrict LDAP port access to application servers only

---

## Additional Resources

- django-auth-ldap documentation: https://django-auth-ldap.readthedocs.io/
- Python LDAP documentation: https://www.python-ldap.org/
- Active Directory LDAP syntax: https://docs.microsoft.com/en-us/windows/win32/adsi/search-filter-syntax
- LDAP filters reference: https://ldap.com/ldap-filters/

---

## Summary

This guide covered:
- ✅ Installing required packages and system dependencies
- ✅ Configuring environment variables
- ✅ Setting up Django settings for LDAP
- ✅ Creating service account in Active Directory
- ✅ Docker Compose integration
- ✅ Testing LDAP authentication
- ✅ Enabling/disabling LDAP
- ✅ Troubleshooting common issues
- ✅ Understanding authentication flow
- ✅ Role assignment process

For additional help or questions, refer to the full-transcript.md or open an issue.
