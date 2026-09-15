import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mebel_erp.settings')
django.setup()

from production.models import Stage

stages = [
    ('Raspil', 1, 2),
    ('Kromka', 2, 3),
    ('Prisadka', 3, 4),
    ('Yigish', 4, 5),
]
for name, order, max_h in stages:
    s, created = Stage.objects.get_or_create(
        name=name,
        defaults={'order': order, 'max_duration_hours': max_h, 'is_active': True}
    )
    print(f"{'Created' if created else 'Exists'}: {name}")

print("Done!")
