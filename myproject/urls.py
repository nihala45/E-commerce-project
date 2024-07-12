"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('adminside/', include('adminside.urls')),
    path('cartapp/', include('cartapp.urls')),
    path('category/', include('category.urls')),
    path('checkout/', include('checkout.urls')),
    path('', include('logintohome.urls')),
    path('productdetail/', include('productdetail.urls')),
    path('products/', include('products.urls')),
    path('usermanagement/', include('usermanagement.urls')),
    path('userprofile/', include('userprofile.urls')),
    path('ordermanagement/', include('ordermanagement.urls')),
    
    
]
urlpatterns +=  static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)