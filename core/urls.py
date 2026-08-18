"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path , include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from marketplace  import views as marketplaceViews
from user_accounts import views as account_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home , name="home"),
    path("", include("user_accounts.urls")),
    path("vendor/",include("vendor_app.urls")),
    path('customer/',include('customers.urls')),

    path('marketplace/',include('marketplace.urls')),
    path('cart/',marketplaceViews.cart, name='cart'),
    # Search 
    path('search/',marketplaceViews.search, name='search'),
    # Chcekout
    path('checkout/', marketplaceViews.checkout , name='checkout'),
    # Orders
   
    # Order funcanilty
    path('orders/' , include('orders.urls')),

    #  APi Routs
    path('api/v1/menu/', include('menu.api_urls')),






    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

