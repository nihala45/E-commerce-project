from django.urls import path
from.import views
from django.contrib.auth.views import LoginView

app_name = "category"

urlpatterns = [
    path('category/',views.categorymanagement,name='category'),
    path('addcategory/',views.addcategory,name='addcategory'),
    path('savecategory/',views.savecategory,name='savecategory'),
    
] 