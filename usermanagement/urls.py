from django.urls import path
from.import views
from django.contrib.auth.views import LoginView

app_name = "usermanagement"

urlpatterns = [
    path('blockuser/<int:user_id>/', views.block_user, name='block_user'),
    path('unblockuser/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('usermanagement/',views.usermanagement,name='usermanagement'),
    
] 