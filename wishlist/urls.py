from django.urls import path
from.import views


app_name = 'wishlist'

urlpatterns = [
    path('Wishlist/', views.Wishlist, name='Wishlist'),

    path('add_to_wishlist/<int:prod_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
]