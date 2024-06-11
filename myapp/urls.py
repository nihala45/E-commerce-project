from django.urls import path
from.import views

urlpatterns = [
    
    path('', views.homee,name='homee'),
    path('login/',views.loginn,name='loginn'),
    path('userlogout/',views.userlogout,name='userlogout'),
    path('shop/',views.shop,name='shop'),
    
    path("otpverification/<str:id>/", views.otp_varification, name="otpverification"),
    path('signup/',views.signupp,name='signup'),
    path('otp/<int:id>/', views.otp, name='otp'), 
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
    # path('edit_category/<int:category_id>/', views.edit_category, name='edit.category'),
    # path('delete_category/<int:category_id>/', views.delete_category, name='delete.category'),
    
] 