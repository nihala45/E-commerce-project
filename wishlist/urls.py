from django.urls import path
from .views import Wishlist, add_to_wishlist

app_name = 'wishlist'

urlpatterns = [
    path('Wishlist/', Wishlist, name='Wishlist'),

    path('add_to_wishlist/<int:prod_id>/', add_to_wishlist, name='add_to_wishlist'),
]