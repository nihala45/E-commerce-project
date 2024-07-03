from django.urls import path
from.import views
from django.contrib.auth.views import LoginView

app_name = "category"

urlpatterns = [
    path('categorymanagement/',views.categorymanagement,name='categorymanagement'),
    path('/',views.categorymanagement,name='categorymanagement'),
    path('savecategory/',views.savecategory,name='savecategory'),
    
    path('addcategory/',views.addcategory,name='addcategory'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('edit_savecategory/', views.edit_savecategory, name='edit_savecategory'),
    path('deletecategory/<int:category_id>/', views.delete_category, name='delete_category'),
] 