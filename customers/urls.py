from django.contrib import admin
from django.urls import path , include
from . import views
from user_accounts import views as account_views

urlpatterns = [ 
    path('',account_views.custmerdashboard , name='customer'),
    path('profile/',views.cust_profile,name='customer_profile'),
    path('my_orders/',views.my_orders,name='cust_my_orders'),
    path('orders_details/<int:order_no>/',views.order_details, name='order_details')
]