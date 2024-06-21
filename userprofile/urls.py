from django.urls import path
from.import views
from django.contrib.auth.views import LoginView

app_name = "userprofile"

urlpatterns = [
    path('signout/', views.signout, name='signout'), 
    path('editprofile/', views.editprofile, name='editprofile'), 
    path('save_edit/',views.save_edit,name='save_edit'),
    # path('save_address/',views.save_address,name='save_address'),
    path('userdashboard/', views.userdashboard, name='userdashboard'), 
    
] 