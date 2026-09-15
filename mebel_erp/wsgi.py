"""
WSGI config for mebel_erp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mebel_erp.settings')

application = get_wsgi_application()

# Auto-migrate and initialize SQLite database on server startup
try:
    from django.core.management import call_command
    from django.contrib.auth.models import User
    from production.models import Stage
    
    print("=== WSGI Startup: Checking / Running Migrations ===", flush=True)
    call_command('migrate', interactive=False)
    
    # Ensure superuser exists
    admin_user = User.objects.filter(username='admin').first()
    if not admin_user:
        print("WSGI Startup: Creating default admin superuser...", flush=True)
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    else:
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        print("WSGI Startup: Admin password verified/updated.", flush=True)

    # Seed initial data if empty
    if Stage.objects.count() == 0:
        print("WSGI Startup: Seeding initial Wood Timbero data...", flush=True)
        import seed_wood_timbero
        print("WSGI Startup: Initial data seeded!", flush=True)
        
    print("=== WSGI Startup: Ready ===", flush=True)
except Exception as e:
    print(f"WSGI Startup Error: {e}", file=sys.stderr, flush=True)
