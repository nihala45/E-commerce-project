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
    path('remove_address/<int:address_id>',views.remove_address,name='remove_address'),
    # path('edit_address/<int:address_id>',views.edit_address,name='edit_address'),
    path('change_password',views.change_password,name='change_password'),
    path('view_details/<int:ord_id>',views.view_details,name='view_details'),
    path('cancelOrder/<int:or_id>',views.cancelOrder,name='cancelOrder'),
    path('edit_address/', views.edit_address, name='edit_address'),
    
    
] 