from django.urls import path
from.import views
from django.contrib.auth.views import LoginView

app_name = "cart"

urlpatterns = [
    path('cart/<int:product_id>/', views.cart, name='cart'),
    path('proceed/',views.proceed,name='proceed'),
    
]