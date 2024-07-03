from django.urls import path
from.import views
from django.contrib.auth.views import LoginView

app_name = "logintohome"

urlpatterns = [
    
    path('', views.homee,name='homee'),
    path('signupp/',views.signupp,name='signupp'),
    path('loginn/',views.loginn,name='loginn'),
    # path('userlogout/',views.userlogout,name='userlogout'),
    path("otpverification/<str:id>/", views.otp_varification, name="otpverification"),
    path('otp/<int:id>/', views.otp, name='otp'), 
    path('shop/',views.shop,name='shop'),
    
    
] 