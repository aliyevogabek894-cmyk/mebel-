from django.db import models
from django.contrib.auth.models import User

class Stage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Bosqich nomi")
    order = models.PositiveIntegerField(verbose_name="Tartib raqami")
    max_duration_hours = models.FloatField(default=0, verbose_name="Maksimal vaqt (soat)")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    description = models.TextField(blank=True, null=True, verbose_name="Izoh")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Employee(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Super Admin'),
        ('MANAGER', 'Rahbar'),
        ('DISPATCHER', 'Dispetcher / Operator'),
        ('WORKER', 'Ishchi'),
        ('INSPECTOR', 'Nazoratchi'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    full_name = models.CharField(max_length=255, verbose_name="F.I.Sh.")
    phone = models.CharField(max_length=50, verbose_name="Telefon")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="Lavozim")
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Biriktirilgan bosqich")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")

    def __str__(self):
        return self.full_name


class Order(models.Model):
    PRIORITY_CHOICES = [
        ('NORMAL', '🟢 Oddiy'),
        ('MEDIUM', '🟡 O‘rtacha'),
        ('HIGH', '🔴 Yuqori'),
        ('URGENT', '⚫ Shoshilinch'),
    ]

    order_number = models.CharField(max_length=50, unique=True, verbose_name="Buyurtma №")
    client_name = models.CharField(max_length=255, verbose_name="Mijoz F.I.Sh.")
    client_phone = models.CharField(max_length=50, verbose_name="Telefon raqami")
    product_type = models.CharField(max_length=100, verbose_name="Mahsulot turi")
    product_name = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    dimensions = models.CharField(max_length=100, blank=True, null=True, verbose_name="O‘lchamlari")
    material = models.CharField(max_length=100, blank=True, null=True, verbose_name="Material")
    color = models.CharField(max_length=100, blank=True, null=True, verbose_name="Material rangi")
    hardware = models.CharField(max_length=255, blank=True, null=True, verbose_name="Furnitura")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Soni")
    manager = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='managed_orders', verbose_name="Mas'ul menejer")
    notes = models.TextField(blank=True, null=True, verbose_name="Izoh")
    deadline = models.DateTimeField(verbose_name="Muddat")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='NORMAL', verbose_name="Ustuvorlik")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    current_stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_orders', verbose_name="Joriy bosqich")
    is_completed = models.BooleanField(default=False, verbose_name="Tayyor")

    def __str__(self):
        return f"#{self.order_number} - {self.client_name}"


class OrderStageHistory(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Yangi'),
        ('IN_PROGRESS', 'Jarayonda'),
        ('WAITING', 'Kutmoqda'),
        ('DELAYED', 'Kechikkan'),
        ('PROBLEM', 'Muammoli'),
        ('CANCELED', 'Bekor qilingan'),
        ('COMPLETED', 'Tayyor'),
        ('PAUSED', 'Pauza'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='stage_history')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    worker = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"{self.order.order_number} - {self.stage.name}"


class Problem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='problems')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    worker = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    reason = models.CharField(max_length=255, verbose_name="Sabab")
    description = models.TextField(blank=True, null=True, verbose_name="Izoh")
    reported_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Muammo: {self.order.order_number} - {self.reason}"


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action}"
