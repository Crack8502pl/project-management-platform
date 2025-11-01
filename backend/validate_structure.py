#!/usr/bin/env python
"""
Script to validate the Django project structure.
"""
import os
import sys

def check_file_exists(path, description):
    """Check if file exists."""
    if os.path.exists(path):
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - Missing: {path}")
        return False

def main():
    """Main validation function."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    
    print("Validating Django Project Structure...")
    print("=" * 60)
    
    all_ok = True
    
    # Check core files
    print("\nCore Files:")
    all_ok &= check_file_exists("manage.py", "manage.py")
    all_ok &= check_file_exists("requirements/base.txt", "requirements/base.txt")
    all_ok &= check_file_exists("requirements/development.txt", "requirements/development.txt")
    all_ok &= check_file_exists("Dockerfile", "Dockerfile")
    all_ok &= check_file_exists("entrypoint.sh", "entrypoint.sh")
    
    # Check config
    print("\nConfig Files:")
    all_ok &= check_file_exists("config/__init__.py", "config/__init__.py")
    all_ok &= check_file_exists("config/settings/base.py", "config/settings/base.py")
    all_ok &= check_file_exists("config/settings/development.py", "config/settings/development.py")
    all_ok &= check_file_exists("config/settings/production.py", "config/settings/production.py")
    all_ok &= check_file_exists("config/urls.py", "config/urls.py")
    all_ok &= check_file_exists("config/wsgi.py", "config/wsgi.py")
    all_ok &= check_file_exists("config/celery.py", "config/celery.py")
    
    # Check apps
    apps = [
        'authentication', 'projects', 'tasks', 'bom',
        'devices', 'ipam', 'documents', 'statistics', 'installation'
    ]
    
    print("\nDjango Apps:")
    for app in apps:
        print(f"\n  {app}:")
        all_ok &= check_file_exists(f"apps/{app}/__init__.py", f"    __init__.py")
        all_ok &= check_file_exists(f"apps/{app}/models.py", f"    models.py")
        all_ok &= check_file_exists(f"apps/{app}/views.py", f"    views.py")
        all_ok &= check_file_exists(f"apps/{app}/serializers.py", f"    serializers.py")
        all_ok &= check_file_exists(f"apps/{app}/urls.py", f"    urls.py")
        all_ok &= check_file_exists(f"apps/{app}/admin.py", f"    admin.py")
        all_ok &= check_file_exists(f"apps/{app}/apps.py", f"    apps.py")
    
    # Check management commands
    print("\nManagement Commands:")
    all_ok &= check_file_exists(
        "apps/authentication/management/commands/init_roles.py",
        "init_roles command"
    )
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✓ All checks passed! Structure is valid.")
        return 0
    else:
        print("✗ Some checks failed. Please review the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
