from django.urls import path , include
from . import views
from user_accounts import views as Accountviews

urlpatterns =[
    path('',Accountviews.vendordashboard,name='vendor'),
    path('profile/',views.vprofile,name='vprofile'),
]