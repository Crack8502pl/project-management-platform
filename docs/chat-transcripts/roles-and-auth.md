# Roles and Authentication Guide

Extracted from chat transcript - authentication options and role management.

---

## Overview

This document describes the authentication and authorization system for the Project Management Platform, including LDAP integration, alternative authentication methods, and role assignment processes.

---

## Authentication Options

The platform supports multiple authentication approaches:

### 1. LDAP/Active Directory Authentication

**Current Implementation**

The platform uses `django-auth-ldap` for Active Directory integration.

**How It Works:**
1. User submits username and password to login endpoint
2. Django attempts authentication against Active Directory via LDAP
3. If LDAP authentication succeeds:
   - User account is created/updated in local database
   - User attributes (first name, last name, email) are synced from AD
   - JWT tokens are generated and returned
4. If LDAP authentication fails, fallback to local database authentication
5. User can now access API endpoints with JWT token

**Pros:**
- Simple setup and configuration
- Works well with Windows/Active Directory environments
- Fast authentication
- Direct integration with existing user directory
- Automatic user provisioning on first login
- Password management handled by Active Directory

**Cons:**
- Requires LDAP port (389/636) to be accessible
- Requires dedicated service account with read permissions
- Password is sent to application (though encrypted in transit)
- Less secure than modern SSO protocols

**Configuration:**
- See [ldap-setup.md](ldap-setup.md) for complete setup instructions
- Environment variables in `.env` file
- Django settings in `config/settings/base.py`

**When to Use:**
- Internal applications within corporate network
- Windows/Active Directory environments
- When simple authentication is needed
- When SSO infrastructure is not available

---

### 2. SAML/SSO Authentication

**Not Currently Implemented** - Future Enhancement

SAML (Security Assertion Markup Language) provides enterprise Single Sign-On capabilities.

**How It Would Work:**
1. User accesses application
2. Application redirects to SAML Identity Provider (IdP)
3. User authenticates with IdP (e.g., ADFS, Azure AD, Okta)
4. IdP generates SAML assertion
5. User redirected back to application with assertion
6. Application validates assertion and creates session

**Pros:**
- More secure than LDAP (no password sent to application)
- Industry standard for enterprise SSO
- Supports multiple identity providers
- Centralized authentication and session management
- Support for multi-factor authentication (MFA)
- Better audit and compliance capabilities

**Cons:**
- More complex setup and configuration
- Requires SAML Identity Provider (IdP)
- Requires SSL/HTTPS
- More difficult to troubleshoot
- May require additional licenses

**Implementation Requirements:**

1. **Install SAML Package:**
   ```bash
   pip install python3-saml
   # or
   pip install djangosaml2
   ```

2. **Configure Django Settings:**
   ```python
   INSTALLED_APPS += ['djangosaml2']
   
   AUTHENTICATION_BACKENDS = [
       'djangosaml2.backends.Saml2Backend',
       'django.contrib.auth.backends.ModelBackend',
   ]
   ```

3. **Set Up Identity Provider (IdP):**
   - Azure AD
   - ADFS (Active Directory Federation Services)
   - Okta
   - OneLogin
   - Auth0

4. **Configure Service Provider (SP) Metadata:**
   - Entity ID
   - Assertion Consumer Service (ACS) URL
   - Single Logout Service (SLS) URL
   - X.509 certificates

**When to Use:**
- Enterprise environments with existing SAML infrastructure
- When enhanced security is required
- Multi-factor authentication needed
- Compliance requirements (SOC2, HIPAA, etc.)
- Multiple applications with SSO

---

### 3. OAuth 2.0 / OpenID Connect

**Not Currently Implemented** - Future Enhancement

Modern authentication protocol used by social providers and enterprise IdPs.

**How It Would Work:**
1. User clicks "Login with Azure AD" (or other provider)
2. Redirected to OAuth provider
3. User authenticates and grants permissions
4. Provider returns authorization code
5. Application exchanges code for access token
6. Application retrieves user info with access token

**Pros:**
- Modern, widely adopted standard
- Support for social logins (Google, GitHub, Microsoft)
- Support for mobile and SPA applications
- Delegated authorization (scopes/permissions)
- Refresh tokens for long-lived sessions

**Cons:**
- Requires OAuth provider configuration
- Need to manage client secrets
- Token management complexity
- Different implementations by providers

**Popular Providers:**
- Azure AD / Microsoft 365
- Google Workspace
- GitHub
- GitLab
- Auth0
- Okta

**Implementation Options:**

1. **django-allauth:**
   ```python
   INSTALLED_APPS += [
       'allauth',
       'allauth.account',
       'allauth.socialaccount',
       'allauth.socialaccount.providers.azure',
       'allauth.socialaccount.providers.github',
   ]
   ```

2. **Python Social Auth:**
   ```python
   INSTALLED_APPS += ['social_django']
   ```

**When to Use:**
- Need social login integration
- Modern cloud-first environments
- Mobile or single-page applications
- When users have accounts with supported providers

---

### 4. Local Database Authentication

**Currently Implemented** - Default Fallback

Standard Django authentication using local database.

**How It Works:**
1. User account stored in PostgreSQL database
2. Password hashed using Argon2 (secure hashing algorithm)
3. User submits credentials to login endpoint
4. Django validates password against stored hash
5. JWT tokens generated on successful authentication

**Pros:**
- Simple, no external dependencies
- Works offline
- Full control over user management
- Fast authentication
- No additional infrastructure needed

**Cons:**
- Need to manage password resets
- No centralized user directory
- Manual user provisioning
- Each application has separate user base

**Password Security:**
- Uses Argon2 hashing algorithm (recommended by OWASP)
- Configurable password requirements
- Support for password history
- Automatic password expiration (if configured)

**When to Use:**
- Development and testing
- Small teams without enterprise authentication
- Fallback when external authentication unavailable
- Administrative/emergency access accounts

---

### 5. Hybrid Approach (Recommended)

**Currently Implemented**

Combine multiple authentication methods for flexibility.

**Configuration:**
```python
AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',      # Try LDAP first
    'django.contrib.auth.backends.ModelBackend',  # Fallback to local DB
]
```

**Benefits:**
- LDAP for regular users
- Local accounts for administrators
- Emergency access when LDAP unavailable
- Service accounts and API keys in local database
- Flexibility for different user types

**Best Practices:**
1. Use LDAP for regular employees
2. Create local admin account as backup
3. Disable local accounts when not needed
4. Monitor authentication sources in logs
5. Document which accounts are local vs LDAP

---

## User Roles System

### Available Roles

The platform has five predefined roles:

1. **Administrator**
   - Full system access and configuration
   - User and role management
   - System settings
   - All CRUD operations on all resources
   - Access to Django Admin panel

2. **Manager**
   - Project management and team coordination
   - Create and assign tasks
   - View team performance metrics
   - Manage project resources
   - Limited administrative functions

3. **Engineer**
   - Technical task management and device configuration
   - BOM creation and management
   - Device configuration
   - IP address management
   - Technical documentation

4. **Technician**
   - Field work and checklist management
   - Update task status
   - Complete installation checklists
   - Upload photos and documents
   - View assigned tasks

5. **Viewer**
   - Read-only access to projects and documentation
   - View project status and reports
   - No modification permissions
   - Useful for stakeholders and auditors

### Role Initialization

Roles are created using the `init_roles` management command:

```bash
docker-compose exec backend python manage.py init_roles
```

This command:
- Creates the five predefined roles if they don't exist
- Safe to run multiple times (idempotent)
- Should be run after initial database migration

---

## Role Assignment Process

### Important: Roles Are NOT Synced from Active Directory

**Key Point:** User roles are managed independently of AD group memberships.

**Why Not Sync from AD?**

1. **Security:** Prevents unauthorized role escalation through AD group manipulation
2. **Flexibility:** Application roles may not map directly to AD groups
3. **Control:** Requires explicit administrator approval
4. **Separation of Concerns:** AD manages authentication, application manages authorization
5. **Audit Trail:** Changes to roles are tracked in application database

### How Role Assignment Works

**When User Logs In via LDAP (First Time):**

1. User authenticates successfully against Active Directory
2. Django creates local user account with:
   - Username (from sAMAccountName)
   - First name (from givenName)
   - Last name (from sn)
   - Email (from mail)
   - **No role assigned** (or default role if configured)
3. User can log in but has minimal permissions
4. Administrator must assign role manually

**Manual Role Assignment:**

1. Administrator logs into Django Admin: http://localhost:8000/admin
2. Navigate to **Users** section
3. Find the user (search by username or email)
4. Click on username to edit
5. In the user edit form:
   - Find the "Role" dropdown field
   - Select appropriate role (Administrator, Manager, Engineer, Technician, or Viewer)
   - Click "Save" button
6. User will have assigned permissions on next login/token refresh

**Programmatic Role Assignment (via API):**

```python
from django.contrib.auth import get_user_model
from apps.users.models import Role

User = get_user_model()
user = User.objects.get(username='john.doe')
engineer_role = Role.objects.get(name='Engineer')
user.role = engineer_role
user.save()
```

**Bulk Role Assignment (Django Shell):**

```bash
docker-compose exec backend python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from apps.users.models import Role

User = get_user_model()
Role = Role.objects.get(name='Technician')

# Assign role to multiple users
usernames = ['user1', 'user2', 'user3']
for username in usernames:
    user = User.objects.get(username=username)
    user.role = role
    user.save()
    print(f"Assigned {role.name} to {username}")
```

---

## Role-Based Access Control (RBAC)

### How Permissions Work

Django's permission system is enhanced with role-based access:

1. **Model Permissions:** 
   - Create (add_modelname)
   - Read (view_modelname)
   - Update (change_modelname)
   - Delete (delete_modelname)

2. **Role-Based Permissions:**
   - Assigned to roles, not individual users
   - Inherited by all users with that role
   - Managed through Django Admin

3. **Custom Permissions:**
   - Application-specific permissions
   - Defined in model Meta class
   - Example: `can_approve_project`, `can_assign_tasks`

### Checking Permissions in Code

**In Views:**
```python
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsAdministrator, IsManagerOrAbove

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsManagerOrAbove]
```

**In View Logic:**
```python
def my_view(request):
    if request.user.role.name == 'Administrator':
        # Admin-only logic
        pass
    elif request.user.role.name in ['Administrator', 'Manager']:
        # Manager and above
        pass
```

**In Templates:**
```django
{% if user.role.name == 'Administrator' %}
    <a href="{% url 'admin:index' %}">Admin Panel</a>
{% endif %}
```

**Object-Level Permissions:**
```python
from apps.projects.models import Project

def can_edit_project(user, project):
    # Administrators can edit any project
    if user.role.name == 'Administrator':
        return True
    # Managers can edit their own projects
    if user.role.name == 'Manager' and project.manager == user:
        return True
    return False
```

---

## Default Permissions by Role

### Administrator
- All permissions (superuser-level access)
- User management
- Role assignment
- System configuration
- All CRUD operations

### Manager
- Create/edit/delete projects
- Assign tasks to team members
- View all team tasks
- Approve timesheets
- Generate reports

### Engineer
- Create/edit technical tasks
- Manage BOM items
- Configure devices
- Manage IP addresses
- Upload technical documentation

### Technician
- View assigned tasks
- Update task status
- Complete checklists
- Upload photos
- Add work logs

### Viewer
- Read-only access to all resources
- View projects and tasks
- View reports
- No create/edit/delete permissions

---

## Security Considerations

### Password Policies

Configure in Django settings:

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

### JWT Token Security

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}
```

### Session Security

```python
SESSION_COOKIE_SECURE = True  # HTTPS only
SESSION_COOKIE_HTTPONLY = True  # No JavaScript access
SESSION_COOKIE_SAMESITE = 'Strict'  # CSRF protection
SESSION_COOKIE_AGE = 3600  # 1 hour
```

### LDAP Security

- Use LDAPS (SSL/TLS) when possible: `ldaps://dc.example.local:636`
- Secure service account password
- Limit service account permissions (read-only)
- Monitor authentication logs
- Implement rate limiting on login endpoint

---

## Authentication Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         User Login                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              POST /api/auth/login/                          │
│              {username, password}                           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│        Django Authentication Backends                       │
│        (tried in order)                                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
         ┌───────────────────────────┐
         │   LDAPBackend              │
         │   ├─ Bind to LDAP server   │
         │   ├─ Search for user       │
         │   ├─ Bind as user          │
         │   └─ Create/update user    │
         └───────────┬───────────────┘
                     │
        Success ────►│◄──── Failure
             │       │           │
             │       ▼           ▼
             │  ┌─────────────────────────┐
             │  │   ModelBackend          │
             │  │   ├─ Check local DB     │
             │  │   └─ Verify password    │
             │  └────────┬────────────────┘
             │           │
             │  Success ─┤
             ▼           │
     ┌───────────────────▼───────┐  Failure
     │  Generate JWT Tokens      │──────────►┌──────────────┐
     │  - Access Token           │           │ Return 401   │
     │  - Refresh Token          │           │ Unauthorized │
     └──────────┬────────────────┘           └──────────────┘
                │
                ▼
     ┌──────────────────────────┐
     │  Return Response:        │
     │  - access token          │
     │  - refresh token         │
     │  - user info (with role) │
     └──────────────────────────┘
```

---

## Troubleshooting Authentication Issues

### User Can Login But Has No Permissions

**Symptom:** User logs in successfully but gets "Permission denied" errors

**Cause:** No role assigned to user

**Solution:**
1. Login to Django Admin
2. Navigate to Users
3. Find the user
4. Assign appropriate role
5. Ask user to logout and login again

### LDAP Authentication Not Working

**Symptom:** "Invalid credentials" error even with correct AD password

**Causes and Solutions:**

1. **LDAP server unreachable:**
   ```bash
   docker-compose exec backend python manage.py test_ldap username
   ```

2. **Service account credentials incorrect:**
   - Verify LDAP_BIND_DN and LDAP_BIND_PASSWORD in `.env`

3. **User not in search base:**
   - Check LDAP_USER_SEARCH_BASE includes user's OU

4. **User's AD account locked/disabled:**
   - Check account status in Active Directory

### JWT Token Expired

**Symptom:** "Token is invalid or expired" error

**Solution:** Use refresh token to get new access token:
```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "refresh_token_here"}'
```

---

## Best Practices

1. **Use Hybrid Authentication:**
   - LDAP for regular users
   - Local admin account as backup

2. **Regular Permission Audits:**
   - Review user roles quarterly
   - Remove inactive users
   - Verify role assignments

3. **Principle of Least Privilege:**
   - Assign minimum required role
   - Use Viewer role for read-only needs
   - Limit Administrator role

4. **Document Role Assignments:**
   - Keep record of who has what role
   - Document approval process
   - Track role changes

5. **Monitor Authentication:**
   - Log all authentication attempts
   - Alert on repeated failures
   - Track role assignment changes

6. **Secure Service Accounts:**
   - Strong, random passwords
   - Read-only permissions
   - Separate account per application
   - Regular password rotation

---

## Summary

This guide covered:
- ✅ Authentication options: LDAP, SAML, OAuth, Local, Hybrid
- ✅ Pros and cons of each authentication method
- ✅ Five user roles: Administrator, Manager, Engineer, Technician, Viewer
- ✅ Why roles are NOT synced from Active Directory
- ✅ How to assign roles manually in Django Admin
- ✅ Role-based access control (RBAC) implementation
- ✅ Security considerations and best practices
- ✅ Troubleshooting authentication issues

For LDAP setup details, see [ldap-setup.md](ldap-setup.md)
