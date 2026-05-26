from django.urls import  include,path
from . import api_view
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register("category", api_view.category_view , basename="category")

urlpatterns = [
    path("category/",api_view.category_view,name='category'),
    path("category/<int:pk>",api_view.categ_details_view)
]