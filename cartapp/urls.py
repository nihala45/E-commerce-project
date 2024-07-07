from django.urls import path
from.import views
from django.contrib.auth.views import LoginView

app_name = "cartapp"

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart_view/', views.cart_view, name='cart_view'),
    path('quantity_upadate/', views.quantity_upadate, name='quantity_upadate'),
    path('proceed_to_checkout/', views.proceed_to_checkout, name='proceed_to_checkout'),
    path('place_order/', views.place_order, name='place_order'),
    
    
    # path('proceed/',views.proceed,name='proceed'),
    
]