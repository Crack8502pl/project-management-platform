"""
Sygnały dla synchronizacji użytkowników z LDAP/AD
"""
from django.dispatch import receiver
from django_auth_ldap.backend import populate_user
from django.utils import timezone
import logging

logger = logging.getLogger('ldap_auth')


@receiver(populate_user)
def ldap_user_populated(sender, user, ldap_user, **kwargs):
    """
    Callback wykonywany po pomyślnym logowaniu przez LDAP.
    Synchronizuje dane z AD i oznacza źródło autentykacji.
    """
    logger.info(f"LDAP user populated: {user.username}")
    
    user.auth_source = 'AD'
    user.ldap_dn = ldap_user.dn
    user.ad_synced_at = timezone.now()
    
    if hasattr(ldap_user, 'attrs'):
        attrs = ldap_user.attrs
        
        if 'telephoneNumber' in attrs:
            phone = attrs['telephoneNumber'][0] if attrs['telephoneNumber'] else ''
            if phone:
                user.phone = phone.decode('utf-8') if isinstance(phone, bytes) else phone
    
    user.save()
    
    logger.info(f"✅ User {user.username} synced from AD (DN: {user.ldap_dn})")
    
    if not user.role:
        logger.warning(f"⚠️  User {user.username} has no role assigned!")
