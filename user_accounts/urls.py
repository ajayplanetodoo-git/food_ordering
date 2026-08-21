from django.urls import path , include
from . import views
from . import api_view


urlpatterns =[
    path('',views.myaccount),
    path("registeruser/", views.registeruser, name="userregister" ),
    path("registerapiuser/", api_view.registeruserapi, name='registerapiuser'),
    path("registervendor/", views.registervendor, name="vendorregister" ),
    path("registerapivendor/", api_view.registervendorapi, name="registerapivendor" ),

    path("myaccount/",views.myaccount , name="myaccount"),
    path("login/", views.login, name="login" ),
    path("logout/", views.logout, name="logout" ),

    path("custdashboard/", views.custmerdashboard, name="custdashboard" ),
    path("venddashboard/", views.vendordashboard, name="vendashboard" ),
    path('activate/<uiddb64>/<token>/',views.activate, name='activate'),


    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_paasword_validate/<uiddb64>/<token>',views.reset_password_validate,name='reset_password_validate'),
    path('reset_password/',views.reset_password,name='reset_password'),

    path('vendor/',include('vendor_app.urls')),
    path('customer/', include('customers.urls')),

    

]