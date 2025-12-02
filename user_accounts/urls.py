from django.urls import path , include
from . import views

urlpatterns =[
    path("registeruser/", views.registeruser, name="userregister" ),
    path("registervendor/", views.registervendor, name="vendorregister" ),

    path("login/", views.login, name="login" ),
    path("logout/", views.logout, name="logout" ),
    path("dashboard/", views.dashboard, name="dashboard" ),


    
]