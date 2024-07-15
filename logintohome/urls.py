from django.urls import path
from.import views
from django.contrib.auth.views import LoginView

app_name = "logintohome"

urlpatterns = [
    
    path('', views.homee,name='homee'),
    path('Signup/',views.Signup,name='Signup'),
    path('loginn/',views.loginn,name='loginn'),
    # path('userlogout/',views.userlogout,name='userlogout'),
    path("otpverification/<str:id>/", views.otp_varification, name="otpverification"),
    path('otp/<int:id>/', views.otp, name='otp'), 
    path('shop/',views.shop,name='shop'),
    path('shop_to_home/',views.shop_to_home,name='shop_to_home'),
    # path('search_items/',views.search_items,name='search_items'),
    path('filterProduct/',views.filterProduct,name='filterProduct'),
    
    
    
    
    
] 