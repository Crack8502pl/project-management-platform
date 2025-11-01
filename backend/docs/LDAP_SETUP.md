# LDAP/Active Directory Integration

## Overview
This backend supports authentication via Active Directory using LDAP protocol, with fallback to local database authentication.

## Configuration

### Environment Variables
Set these in your `.env` file:
- `LDAP_SERVER_URI` - LDAP server URI (e.g., ldap://dc.example.local:389)
- `LDAP_BIND_DN` - Service account Distinguished Name
- `LDAP_BIND_PASSWORD` - Service account password
- `LDAP_USER_SEARCH_BASE` - Base DN for user search

### Active Directory Requirements
1. Create a service account with read permissions
2. Ensure LDAP port (389) is accessible from backend server
3. Users should exist in AD with proper attributes (givenName, sn, mail)

## Testing
Test LDAP connection:
```bash
docker-compose exec backend python manage.py test_ldap username
```

## Authentication Flow
1. User submits username/password
2. Django checks AD via LDAP (if configured)
3. If not found in AD, checks local database
4. On success, returns JWT token
5. Role assignment is done manually in Django Admin

## Role Assignment
Roles are NOT synced from AD groups. Administrator must assign roles manually:
1. User logs in for the first time (created from AD)
2. Admin goes to Django Admin → Users
3. Assigns appropriate role
4. User has full access on next login
