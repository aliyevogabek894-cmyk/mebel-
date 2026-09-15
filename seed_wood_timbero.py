import os
import django
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mebel_erp.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from production.models import Stage, Employee, Order, OrderStageHistory, Problem, AuditLog

print("Updating stages...")
# Stages matching the design mockups: Kesish (arra), Kromka, Prisatka
stage_defs = [
    ("Kesish (arra)", 1, 2.0),
    ("Kromka", 2, 2.5),
    ("Prisatka", 3, 3.0),
]

stages_map = {}
for name, order, max_h in stage_defs:
    stage, _ = Stage.objects.update_or_create(
        order=order,
        defaults={'name': name, 'max_duration_hours': max_h, 'is_active': True}
    )
    stages_map[name] = stage

# Also delete or deactivate any stage with order > 3
Stage.objects.filter(order__gt=3).delete()

print("Stages updated:", [s.name for s in Stage.objects.all()])

print("Updating users and employees...")
# Admin
admin_user, _ = User.objects.get_or_create(username='admin')
admin_user.set_password('admin123')
admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.save()

emp_admin, _ = Employee.objects.update_or_create(
    user=admin_user,
    defaults={'full_name': 'Operator Admin', 'phone': '+998 90 000-00-01', 'role': 'ADMIN'}
)

# Arrachi
arrachi_user, _ = User.objects.get_or_create(username='arrachi')
arrachi_user.set_password('arrachi123')
arrachi_user.save()
emp_arrachi, _ = Employee.objects.update_or_create(
    user=arrachi_user,
    defaults={'full_name': 'Arrachi Operator', 'phone': '+998 90 111-22-33', 'role': 'WORKER', 'stage': stages_map["Kesish (arra)"]}
)

# Kromkachi
kromkachi_user, _ = User.objects.get_or_create(username='kromkachi')
kromkachi_user.set_password('kromkachi123')
kromkachi_user.save()
emp_kromkachi, _ = Employee.objects.update_or_create(
    user=kromkachi_user,
    defaults={'full_name': 'Kromkachi Usta', 'phone': '+998 90 444-55-66', 'role': 'WORKER', 'stage': stages_map["Kromka"]}
)

# Prisatkachi
prisatka_user, _ = User.objects.get_or_create(username='prisatka')
prisatka_user.set_password('prisatka123')
prisatka_user.save()
emp_prisatka, _ = Employee.objects.update_or_create(
    user=prisatka_user,
    defaults={'full_name': 'Prisatka Mutaxassisi', 'phone': '+998 90 777-88-99', 'role': 'WORKER', 'stage': stages_map["Prisatka"]}
)

print("Employees configured.")

print("Populating orders to match 24 orders (8 Tayyor, 12 Jarayonda, 4 Kutilmoqda)...")
OrderStageHistory.objects.all().delete()
Problem.objects.all().delete()
AuditLog.objects.all().delete()
Order.objects.all().delete()

now = timezone.now()

raw_orders = [
    # Tayyor (8 ta)
    ("001", "M-001", "Ali", "+998 90 123-45-67", "Oshxona garnituri", "LDSP 18 mm", "2800 × 600 mm", "Yong'oq", "Blum", 2, "Eshiklar alohida, profil tutqich", "COMPLETED", None),
    ("002", "M-002", "Jamshid", "+998 91 234-56-78", "Shkaf-kupe", "MDF 16 mm", "2400 × 1200 mm", "Oq mat", "GTV", 1, "Ko'zgu bilan", "IN_PROGRESS", "Kromka"),
    ("003", "M-003", "Aziz", "+998 93 345-67-89", "Yotoqxona to'plami", "LDSP 18 mm", "2000 × 900 mm", "Kulrang", "Boyard", 1, "Kromka 2mm bo'lsin", "IN_PROGRESS", "Kesish (arra)"),
    ("004", "M-004", "Sohib", "+998 94 456-78-90", "Ofis stoli", "LDSP 25 mm", "1600 × 800 mm", "Dub sonoma", "Blum", 4, "Kabel kanali ochilsin", "IN_PROGRESS", "Kromka"),
    ("005", "M-005", "Dilshod", "+998 95 567-89-01", "Tv tumba", "MDF 18 mm", "1800 × 450 mm", "Qora mat", "Hafele", 1, "Teshiklar tayyor bo'lishi kerak", "WAITING", "Kesish (arra)"),
    ("006", "M-006", "Rustam", "+998 97 678-90-12", "Dahliz mebeli", "LDSP 18 mm", "2200 × 1000 mm", "Antratsit", "Boyard", 1, "Ildizli ilgaklar", "COMPLETED", None),

    # More Tayyor (jami 8)
    ("007", "M-007", "Baxrom", "+998 90 789-01-23", "Bolalar xonasi stoli", "LDSP 18 mm", "1200 × 600 mm", "Sariq/Oq", "GTV", 1, "", "COMPLETED", None),
    ("008", "M-008", "Zarif", "+998 91 890-12-34", "Kiyim shkafi", "LDSP 18 mm", "2400 × 1800 mm", "Wenge", "Blum", 1, "", "COMPLETED", None),
    ("009", "M-009", "Farhod", "+998 93 901-23-45", "Kassa peshtaxtasi", "LDSP 25 mm", "1500 × 700 mm", "Grafir", "Hafele", 2, "", "COMPLETED", None),
    ("010", "M-010", "Ulug'bek", "+998 94 012-34-56", "Restoran stollari", "Massiv eman", "800 × 800 mm", "Tabiiy", "Boyard", 6, "", "COMPLETED", None),
    ("011", "M-011", "Jasur", "+998 95 123-45-67", "Jurnal stoli", "MDF bo'yoq", "900 × 500 mm", "Marmar naqsh", "Blum", 1, "", "COMPLETED", None),
    ("012", "M-012", "Nodir", "+998 97 234-56-78", "Kutubxona javoni", "LDSP 18 mm", "2600 × 2000 mm", "Dub", "GTV", 1, "", "COMPLETED", None),

    # More Jarayonda (jami 12)
    ("013", "M-013", "Shohruh", "+998 90 345-67-89", "Oshxona oroli", "MDF akril", "2100 × 900 mm", "Yashil mat", "Blum", 1, "", "IN_PROGRESS", "Prisatka"),
    ("014", "M-014", "Komil", "+998 91 456-78-90", "Oyoq kiyim javoni", "LDSP 16 mm", "1100 × 800 mm", "Kulrang", "Boyard", 2, "", "IN_PROGRESS", "Kesish (arra)"),
    ("015", "M-015", "Otabek", "+998 93 567-89-01", "Krovat karkasi", "LDSP 25 mm", "2000 × 1800 mm", "Dub sonoma", "Hafele", 1, "", "IN_PROGRESS", "Prisatka"),
    ("016", "M-016", "Sanjar", "+998 94 678-90-12", "Reception stoli", "MDF bo'yoq", "2400 × 1100 mm", "Moviy mat", "Blum", 1, "", "IN_PROGRESS", "Kromka"),
    ("017", "M-017", "Mansur", "+998 95 789-01-23", "Boshliq stoli", "LDSP 36 mm", "1800 × 900 mm", "Oreh", "GTV", 1, "", "IN_PROGRESS", "Kesish (arra)"),
    ("018", "M-018", "Bekzod", "+998 97 890-12-34", "Balkon shkafi", "LDSP 16 mm", "2500 × 850 mm", "Oq", "Boyard", 1, "", "IN_PROGRESS", "Kromka"),
    ("019", "M-019", "Davron", "+998 90 901-23-45", "Vitrina shkafi", "MDF + Shisha", "2000 × 600 mm", "Qora profil", "Blum", 2, "", "IN_PROGRESS", "Prisatka"),
    ("020", "M-020", "Qobil", "+998 91 012-34-56", "Restoran barmaydoni", "LDSP 25 mm", "3200 × 700 mm", "Grafit", "Hafele", 1, "", "IN_PROGRESS", "Kesish (arra)"),
    ("021", "M-021", "Ilhom", "+998 93 123-45-67", "Garderob xonasi", "LDSP 18 mm", "3000 × 2400 mm", "Oq tekstura", "GTV", 1, "", "IN_PROGRESS", "Kromka"),

    # More Kutilmoqda (jami 4)
    ("022", "M-022", "Bobur", "+998 94 234-56-78", "Vanna mebeli", "MDF namga chidamli", "1000 × 500 mm", "Moviy", "Blum", 1, "", "WAITING", "Kesish (arra)"),
    ("023", "M-023", "Muzaffar", "+998 95 345-67-89", "Dars stoli", "LDSP 18 mm", "1300 × 650 mm", "Yashil/Oq", "Boyard", 2, "", "WAITING", "Kesish (arra)"),
    ("024", "M-024", "Javlon", "+998 97 456-78-90", "Terrasa kreslolari", "Massiv qayin", "Standart", "Lakkalangan", "—", 4, "", "WAITING", "Kesish (arra)"),
]

s_kesish = stages_map["Kesish (arra)"]
s_kromka = stages_map["Kromka"]
s_prisatka = stages_map["Prisatka"]

for num, ord_num, client, phone, prod_name, mat, dim, col, hard, qty, note, status_type, stage_name in raw_orders:
    is_comp = (status_type == "COMPLETED")
    curr_stage = stages_map.get(stage_name) if stage_name else (None if is_comp else s_kesish)

    order = Order.objects.create(
        order_number=ord_num.replace("M-", ""),
        client_name=client,
        client_phone=phone,
        product_type="Mebel ishlab chiqarish",
        product_name=prod_name,
        dimensions=dim,
        material=mat,
        color=col,
        hardware=hard,
        quantity=qty,
        manager=emp_admin,
        notes=note,
        deadline=now + timedelta(days=2 if not is_comp else -1),
        priority='NORMAL' if num not in ['003', '013'] else 'HIGH',
        current_stage=curr_stage,
        is_completed=is_comp
    )

    if is_comp:
        t1 = now - timedelta(days=2, hours=4)
        t2 = now - timedelta(days=2, hours=2)
        t3 = now - timedelta(days=2, hours=1)
        t4 = now - timedelta(days=2)
        OrderStageHistory.objects.create(order=order, stage=s_kesish, worker=emp_arrachi, status='COMPLETED', start_time=t1, end_time=t2, time_spent=timedelta(hours=2))
        OrderStageHistory.objects.create(order=order, stage=s_kromka, worker=emp_kromkachi, status='COMPLETED', start_time=t2, end_time=t3, time_spent=timedelta(hours=1))
        OrderStageHistory.objects.create(order=order, stage=s_prisatka, worker=emp_prisatka, status='COMPLETED', start_time=t3, end_time=t4, time_spent=timedelta(hours=1))
    elif status_type == "IN_PROGRESS":
        if stage_name == "Kesish (arra)":
            OrderStageHistory.objects.create(order=order, stage=s_kesish, worker=emp_arrachi, status='IN_PROGRESS', start_time=now - timedelta(hours=1))
        elif stage_name == "Kromka":
            OrderStageHistory.objects.create(order=order, stage=s_kesish, worker=emp_arrachi, status='COMPLETED', start_time=now - timedelta(hours=4), end_time=now - timedelta(hours=2))
            OrderStageHistory.objects.create(order=order, stage=s_kromka, worker=emp_kromkachi, status='IN_PROGRESS', start_time=now - timedelta(hours=1))
        elif stage_name == "Prisatka":
            OrderStageHistory.objects.create(order=order, stage=s_kesish, worker=emp_arrachi, status='COMPLETED', start_time=now - timedelta(hours=6), end_time=now - timedelta(hours=4))
            OrderStageHistory.objects.create(order=order, stage=s_kromka, worker=emp_kromkachi, status='COMPLETED', start_time=now - timedelta(hours=4), end_time=now - timedelta(hours=2))
            OrderStageHistory.objects.create(order=order, stage=s_prisatka, worker=emp_prisatka, status='IN_PROGRESS', start_time=now - timedelta(hours=1))
    elif status_type == "WAITING":
        OrderStageHistory.objects.create(order=order, stage=s_kesish, status='NEW')

prob_order = Order.objects.get(order_number="005")
Problem.objects.create(
    order=prob_order,
    stage=s_kesish,
    worker=emp_arrachi,
    reason="Material yetishmovchiligi",
    description="Qo'shimcha 1 dona 18mm list kerak bo'ldi",
    resolved=False
)

print(f"Successfully populated {Order.objects.count()} orders!")
print("Completed count:", Order.objects.filter(is_completed=True).count())
print("Active in-progress count:", Order.objects.filter(is_completed=False, stage_history__status='IN_PROGRESS').distinct().count())
print("Waiting count:", Order.objects.filter(is_completed=False, stage_history__status='NEW').distinct().count())
