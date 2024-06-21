from django.urls import path
from.import views
from django.contrib.auth.views import LoginView

app_name = "productdetails"

urlpatterns = [
    path('productdetails/',views.productdetails,name='productdetails'),
    
]