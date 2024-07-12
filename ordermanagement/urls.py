from django.urls import path
from . import views

app_name = "ordermanagement"

urlpatterns = [
    path('order_management/', views.order_management, name='order_management'),
    path('admin_ordered_view/<int:ord_id>/', views.admin_ordered_view, name='admin_ordered_view'),
    path('status_update/', views.status_update, name='status_update'),
    
]