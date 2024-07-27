from django.urls import path
from . import views

app_name = "couponmanagement"

urlpatterns = [
    path('coupon/', views.coupon, name='coupon'),  
    path('Addcoupon/', views.Addcoupon, name='Addcoupon'),  
    path('remove_coupon/<int:coupon_id>', views.remove_coupon, name='remove_coupon'),  
    path('coupons/<int:coupon_id>/details/',views.get_coupon,name='coupon-details')
    
]