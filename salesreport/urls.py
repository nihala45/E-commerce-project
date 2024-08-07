from django.urls import path
from.import views


app_name = "salesreport"

urlpatterns = [
    
    path('salesReport', views.salesReport,name='salesReport'),
    # path('filterSales', views.filterSales,name='filterSales'),
] 