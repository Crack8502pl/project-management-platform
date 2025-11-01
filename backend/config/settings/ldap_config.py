"""
LDAP Authentication Configuration for Active Directory
"""
import ldap
import os
from django_auth_ldap.config import LDAPSearch, ActiveDirectoryGroupType

# ============================================
# LDAP Server Configuration
# ============================================
AUTH_LDAP_SERVER_URI = os.getenv('LDAP_SERVER_URI', 'ldap://localhost:389')

# Service Account credentials
AUTH_LDAP_BIND_DN = os.getenv('LDAP_BIND_DN', '')
AUTH_LDAP_BIND_PASSWORD = os.getenv('LDAP_BIND_PASSWORD', '')

# ============================================
# User Search Configuration
# ============================================
LDAP_USER_SEARCH_BASE = os.getenv('LDAP_USER_SEARCH_BASE', 'CN=Users,DC=example,DC=local')

AUTH_LDAP_USER_SEARCH = LDAPSearch(
    LDAP_USER_SEARCH_BASE,
    ldap.SCOPE_SUBTREE,
    "(sAMAccountName=%(user)s)"
)

# ============================================
# User Attributes Mapping
# ============================================
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

# ============================================
# Group Configuration
# ============================================
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    LDAP_USER_SEARCH_BASE,
    ldap.SCOPE_SUBTREE,
    "(objectClass=group)"
)

AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType()

# ============================================
# User Creation/Update Settings
# ============================================
AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_MIRROR_GROUPS = False

# ============================================
# Connection Options
# ============================================
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_DEBUG_LEVEL: 1,
    ldap.OPT_REFERRALS: 0,
    ldap.OPT_NETWORK_TIMEOUT: 10,
}

# ============================================
# Cache Settings
# ============================================
AUTH_LDAP_CACHE_TIMEOUT = 3600
