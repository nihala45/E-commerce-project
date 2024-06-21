from django.urls import path
from .import views
from django.contrib.auth.views import LoginView

app_name = "products"

urlpatterns = [
    path('products/',views.products,name='products'),
    path('saveproduct/',views.saveproducts,name='saveproduct'),

    path('addproduct/',views.addproduct,name='addproduct'),
    path('addvarient/',views.addvarient,name='addvarient'),
    # path('edit_category/<int:category_id>/', views.edit_category, name='edit.category'),
    # path('delete_category/<int:category_id>/', views.delete_category, name='delete.category'),
    
] 