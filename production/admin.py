from django.contrib import admin
from .models import Stage, Employee, Order, OrderStageHistory, Problem, AuditLog

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'max_duration_hours', 'is_active')
    list_editable = ('order', 'max_duration_hours', 'is_active')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'role', 'phone', 'stage', 'is_active')
    list_filter = ('role', 'is_active', 'stage')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'client_name', 'product_name', 'priority', 'current_stage', 'deadline', 'is_completed')
    list_filter = ('priority', 'is_completed', 'current_stage')
    search_fields = ('order_number', 'client_name', 'client_phone')

@admin.register(OrderStageHistory)
class OrderStageHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'stage', 'worker', 'status', 'start_time', 'end_time')
    list_filter = ('status', 'stage')

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('order', 'stage', 'worker', 'reason', 'reported_at', 'resolved')
    list_filter = ('resolved', 'stage')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action')
    search_fields = ('action', 'details')
