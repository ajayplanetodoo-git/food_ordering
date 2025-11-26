from django.urls import path , include
from . import views

urlpatterns =[
    path("registeruser/", views.registeruser, name="userregister" ),
]