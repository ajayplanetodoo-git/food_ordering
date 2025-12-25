from django.urls import path , include
from . import views

urlpatterns = [
    path('',views.marketplace,name='marketplace'),
    path('<slug:vendor_slug>/',views.vendor_details,name='vendor_details')
]