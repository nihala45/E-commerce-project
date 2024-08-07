from django.urls import path
from.import views
from django.contrib.auth.views import LoginView
from products.models import newproducts

app_name = "productdetail"

urlpatterns = [
    path('productdetails/<int:id>/', views.productdetails, name='productdetails'),
    path('addToWishlist', views.addToWishlist, name='addToWishlist'),
    
]