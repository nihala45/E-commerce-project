from django.urls import path
from . import views

app_name = "offermanagement"

urlpatterns = [
    path('offermanagement/', views.offermanagement, name='offermanagement'),
    path('Addoffer/', views.Addoffer, name='Addoffer'),
    path('editSubmitOffer/', views.editSubmitOffer, name='editSubmitOffer'),
    path('remove_offer/<int:offer_id>/', views.remove_offer, name='remove_offer'),
    path('get_offer/<int:offer_id>/', views.get_offer, name='get_offer'),
    
    
    
    
    
    ]