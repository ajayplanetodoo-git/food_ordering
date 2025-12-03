from django.urls import path , include
from . import views

urlpatterns =[
    path("registeruser/", views.registeruser, name="userregister" ),
    path("registervendor/", views.registervendor, name="vendorregister" ),
    path("myaccount/",views.myaccount , name="myaccount"),
    path("login/", views.login, name="login" ),
    path("logout/", views.logout, name="logout" ),
    path("custdashboard/", views.custmerdashboard, name="custdashboard" ),
    path("venddashboard/", views.vendordashboard, name="vendashboard" ),


    
]