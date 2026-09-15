import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mebel_erp.settings')
django.setup()

from django.contrib.auth.models import User

# Admin parolini o'rnatish
admin = User.objects.get(username='admin')
admin.set_password('admin123')
admin.save()
print("Admin parol: admin123")

# Test ishchi yaratish
from production.models import Employee, Stage

kromka = Stage.objects.get(name='Kromka')
raspil = Stage.objects.get(name='Raspil')

# Rahbar
if not User.objects.filter(username='rahbar').exists():
    u1 = User.objects.create_user('rahbar', password='rahbar123')
    Employee.objects.create(user=u1, full_name='Sardor Karimov', phone='+998901234567', role='MANAGER')
    print("Rahbar yaratildi: rahbar / rahbar123")

# Ishchi 1
if not User.objects.filter(username='anvar').exists():
    u2 = User.objects.create_user('anvar', password='anvar123')
    Employee.objects.create(user=u2, full_name='Anvar Aliyev', phone='+998901111111', role='WORKER', stage=kromka)
    print("Ishchi yaratildi: anvar / anvar123 (Kromka)")

# Ishchi 2
if not User.objects.filter(username='jasur').exists():
    u3 = User.objects.create_user('jasur', password='jasur123')
    Employee.objects.create(user=u3, full_name='Jasur Sobirov', phone='+998902222222', role='WORKER', stage=raspil)
    print("Ishchi yaratildi: jasur / jasur123 (Raspil)")

# Admin uchun Employee
if not Employee.objects.filter(user=admin).exists():
    Employee.objects.create(user=admin, full_name='Administrator', phone='—', role='ADMIN')
    print("Admin employee yaratildi")

print("Tayyor!")
