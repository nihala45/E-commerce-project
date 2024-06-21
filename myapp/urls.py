from django.urls import path
from.import views
from django.contrib.auth.views import LoginView

app_name = "myapp"

urlpatterns = [
    
    path('', views.homee,name='homee'),
    path('login/',views.loginn,name='loginn'),
    path('userlogout/',views.userlogout,name='userlogout'),
    path('shop/',views.shop,name='shop'),
    
    path("otpverification/<str:id>/", views.otp_varification, name="otpverification"),
    path('signup/',views.signupp,name='signup'),
    path('otp/<int:id>/', views.otp, name='otp'), 
    path('userdashboard/', views.userdashboard, name='userdashboard'), 
    path('signout/', views.signout, name='signout'), 
    path('editprofile/', views.editprofile, name='editprofile'), 
    path('save_edit/',views.save_edit,name='save_edit'),
    path('save_address/',views.save_address,name='save_address'),
    path('productdetails/',views.productdetails,name='productdetails'),
    # path('addvarient/',views.addvarient,name='addvarient'),
    path('cart/',views.cartp,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('proceed/',views.proceed,name='proceed'),
    
    

    
    
   
    
    
    
    # path('resend_otp/<int:id>/', views.resend_otp, name='resend_otp'),
    # path('resendotp/<int:id>/', views.resend_otp, name='resendotp'),
    
    
    # ADMIN SIDE
    path('adminlogin/',views.adminloginn,name='adminlogin'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('usermanagement/',views.usermanagement,name='usermanagement'),
    path('category/',views.categorymanagement,name='category'),
    path('addcategory/',views.addcategory,name='addcategory'),
    path('savecategory/',views.savecategory,name='savecategory'),
    path('products/',views.products,name='products'),
    path('saveproduct/',views.saveproducts,name='saveproduct'),

    path('addproduct/',views.addproduct,name='addproduct'),
    path('logout/',views.logout_view,name='logout'),
    path('blockuser/<int:user_id>/', views.block_user, name='block_user'),
    path('unblockuser/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('addvarient/<int:prod_id>/',views.addvarient,name='addvarient'),
    # path('edit_category/<int:category_id>/', views.edit_category, name='edit.category'),
    # path('delete_category/<int:category_id>/', views.delete_category, name='delete.category'),
    
] 
