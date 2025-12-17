from django.urls import path , include
from . import views
from user_accounts import views as Accountviews

urlpatterns =[
    path('',Accountviews.vendordashboard,name='vendor'),
    path('profile/',views.vprofile,name='vprofile'),
    path('menu-builder/',views.menu_builder,name='menubuilder'),
    path('menu-builder/category/<int:pk>/',views.fooditeams_by_category,name='fooditems_by_category'),
]