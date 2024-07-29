from django.urls import path
from.import views
from django.contrib.auth.views import LoginView

app_name = "cartapp"

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    # path('cart_view/', views.cart_view, name='cart_view'),
    path('quantity_upadate/', views.quantity_upadate, name='quantity_upadate'),
    path('proceed_to_checkout/', views.proceed_to_checkout, name='proceed_to_checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('continue_shopping/', views.continue_shopping, name='continue_shopping'),
    path('show_cart/',views.show_cart,name='show_cart'),
    path('Remove_cart_product/<int:it_id>/',views.Remove_cart_product, name='Remove_cart_product'),
    path('successpage/',views.successpage,name='successpage'),
    path('razor_save/',views.razor_save,name='razor_save'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('none_coupon/', views.none_coupon, name='none_coupon'),
    
    

    
    
    
    
    # path('proceed/',views.proceed,name='proceed'),
    
]