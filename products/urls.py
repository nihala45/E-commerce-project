from django.urls import path
from .import views
from django.contrib.auth.views import LoginView

app_name = "products"

urlpatterns = [
    path('products/',views.products,name='products'),
    path('saveproducts/',views.saveproducts,name='saveproducts'),
    path('popular-items/', views.popular_items, name='popular_items'),
    path('addproduct/',views.addproduct,name='addproduct'),
    path('product_delete/<int:prod_id>/', views.product_delete, name='product_delete'),
    path('product_editpage/<int:prod_id>/',views.product_editpage,name='product_editpage'),
    path('product_editsave/',views.product_editsave,name='product_editsave'),
    path('popular_items/',views.popular_items, name='popular_items'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),  
    # path('search_for_product/',views.search_for_product,name='search_for_product'),
] 