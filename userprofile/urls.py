from django.urls import path
from.import views
from django.contrib.auth.views import LoginView

app_name = "userprofile"

urlpatterns = [
    path('signout/', views.signout, name='signout'), 
    path('editprofile/', views.editprofile, name='editprofile'), 
    path('save_edit/',views.save_edit,name='save_edit'),
    path('add_user_address/',views.add_user_address,name='add_user_address'),
    
    # path('save_address/',views.save_address,name='save_address'),
    path('userdashboard/', views.userdashboard, name='userdashboard'), 
    path('remove_address/<int:address_id>',views.remove_address,name='remove_address')
    
] 