from django.urls import path , include
from .views import registeruser

urlpatterns =[
    path("registeruser/", registeruser, name="userregister" ),
]