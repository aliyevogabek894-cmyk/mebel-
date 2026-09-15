from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet)
router.register(r'stages', views.StageViewSet)

urlpatterns = [
    # Auth
    path('', views.dashboard, name='dashboard'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),

    # Manager views
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/new/', views.order_create, name='order_create'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/move/', views.order_move_stage, name='order_move_stage'),
    path('kanban/', views.kanban, name='kanban'),
    path('problems/', views.problems, name='problems'),
    path('problems/<int:pk>/resolve/', views.resolve_problem, name='resolve_problem'),
    path('workers/', views.workers_list, name='workers_list'),
    path('reports/', views.reports, name='reports'),
    path('architecture/', views.architecture, name='architecture'),

    # Worker views
    path('my-tasks/', views.worker_panel, name='worker_panel'),
    path('my-tasks/completed/', views.worker_completed, name='worker_completed'),
    path('worker-task/<int:pk>/', views.worker_task, name='worker_task'),
    path('orders/<int:pk>/start/', views.worker_start, name='worker_start'),
    path('orders/<int:pk>/complete/', views.worker_complete, name='worker_complete'),
    path('orders/<int:pk>/problem/', views.worker_problem, name='worker_problem'),

    # REST API
    path('api/', include(router.urls)),
]
