from django.urls import path , include
from . import views
from user_accounts import views as Accountviews

urlpatterns =[
    path('',Accountviews.vendordashboard,name='vendor'),
    path('profile/',views.vprofile,name='vprofile'),
    path('menu-builder/category/<int:pk>/', views.fooditeams_by_category, name='fooditems_by_category'),
    path('menu-builder/',views.menu_builder,name='menubuilder'),
#     category curd
    path('menu-builder/category/add/', views.add_category,name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category,name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category,name='delete_category'),
#   fooditeam curd
    path('menu-builder/fooditeam/add/', views.add_fooditeam,name='add_fooditeam'),
    path('menu-builder/fooditeam/edit/<int:pk>/', views.edit_fooditeam,name='views.edit_fooditeam'),
    path('menu-builder/fooditeam/delete/<int:pk>/', views.delete_fooditeam,name='delete_fooditeam'),


]
