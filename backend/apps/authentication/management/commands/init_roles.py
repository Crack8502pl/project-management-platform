from django.core.management.base import BaseCommand
from apps.authentication.models import Role


class Command(BaseCommand):
    help = 'Initialize default roles'

    def handle(self, *args, **kwargs):
        roles_data = [
            {
                'name': 'admin',
                'description': 'Administrator with full system access',
                'permissions': {
                    'can_manage_users': True,
                    'can_manage_projects': True,
                    'can_manage_all_tasks': True,
                    'can_view_reports': True,
                    'can_manage_settings': True,
                }
            },
            {
                'name': 'manager',
                'description': 'Project Manager with project management permissions',
                'permissions': {
                    'can_manage_projects': True,
                    'can_manage_tasks': True,
                    'can_assign_tasks': True,
                    'can_view_reports': True,
                }
            },
            {
                'name': 'engineer',
                'description': 'Engineer with technical permissions',
                'permissions': {
                    'can_view_projects': True,
                    'can_manage_own_tasks': True,
                    'can_update_devices': True,
                    'can_upload_documents': True,
                }
            },
            {
                'name': 'technician',
                'description': 'Technician with field work permissions',
                'permissions': {
                    'can_view_projects': True,
                    'can_view_tasks': True,
                    'can_update_checklists': True,
                    'can_upload_photos': True,
                }
            },
            {
                'name': 'viewer',
                'description': 'Viewer with read-only access',
                'permissions': {
                    'can_view_projects': True,
                    'can_view_tasks': True,
                    'can_view_documents': True,
                }
            },
        ]

        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                name=role_data['name'],
                defaults={
                    'description': role_data['description'],
                    'permissions': role_data['permissions']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created role: {role.get_name_display()}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Role already exists: {role.get_name_display()}')
                )

        self.stdout.write(self.style.SUCCESS('Roles initialization completed!'))
