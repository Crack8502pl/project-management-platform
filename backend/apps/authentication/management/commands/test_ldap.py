from django.core.management.base import BaseCommand
from django_auth_ldap.backend import LDAPBackend
import ldap


class Command(BaseCommand):
    help = 'Test LDAP connection and search'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to test')

    def handle(self, *args, **options):
        username = options['username']
        
        self.stdout.write(f"Testing LDAP connection for user: {username}")
        self.stdout.write("=" * 50)
        
        backend = LDAPBackend()
        
        try:
            self.stdout.write("Connecting to LDAP server...")
            ldap_user = backend.populate_user(username)
            
            if ldap_user:
                self.stdout.write(self.style.SUCCESS("✅ User found in AD!"))
                self.stdout.write(f"DN: {ldap_user.dn}")
                self.stdout.write(f"Attributes:")
                for key, value in ldap_user.attrs.items():
                    self.stdout.write(f"  {key}: {value}")
            else:
                self.stdout.write(self.style.ERROR("❌ User not found in AD"))
                
        except ldap.INVALID_CREDENTIALS:
            self.stdout.write(self.style.ERROR("❌ Invalid LDAP bind credentials"))
        except ldap.SERVER_DOWN:
            self.stdout.write(self.style.ERROR("❌ LDAP server is down or unreachable"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {str(e)}"))
