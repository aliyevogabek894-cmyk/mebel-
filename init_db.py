import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mebel_erp.settings')
django.setup()

from django.contrib.auth.models import User
from production.models import Stage, Employee, Order

def init():
    print("=== Checking Database Initialization ===")
    
    # 1. Ensure admin user exists
    admin_user = User.objects.filter(username='admin').first()
    if not admin_user:
        print("Creating superuser 'admin' with password 'admin123'...")
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        admin_user.save()
        print("Superuser 'admin' created.")
    else:
        # Ensure password is set to admin123
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        print("Superuser 'admin' updated.")

    # 2. Check if stages and orders are seeded
    stage_count = Stage.objects.count()
    order_count = Order.objects.count()
    print(f"Current stages count: {stage_count}, orders count: {order_count}")
    
    if stage_count == 0 or order_count == 0:
        print("Running seed_wood_timbero.py to populate initial furniture production data...")
        try:
            import seed_wood_timbero
            print("Initial furniture data successfully seeded!")
        except Exception as e:
            print(f"Error seeding data: {e}")
    else:
        print("Database already contains data, skipping seed.")

if __name__ == '__main__':
    init()
