from django.urls import path
from.import views
from django.contrib.auth.views import LoginView

app_name = "adminside"

urlpatterns = [
    path('adminlogin/',views.adminloginn,name='adminlogin'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout_view/',views.logout_view,name='logout_view'),
    
]