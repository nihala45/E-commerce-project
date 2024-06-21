from django.urls import path
from.import views
from django.contrib.auth.views import LoginView

app_name = "cart"

urlpatterns = [
    path('cart/',views.cartp,name='cart'),
    path('proceed/',views.proceed,name='proceed'),
    
]