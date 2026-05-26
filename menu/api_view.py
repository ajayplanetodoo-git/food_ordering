from django.shortcuts import get_object_or_404
from pip._internal.utils import retry
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Category, FoodIteam

from .serializers import CategorySerializer, FoodItemSerializer

#  this api point is only for CURD of category app
@api_view(["GET", "POST", ])
def category_view(request):
    if request.method == "GET":
        category = Category.objects.all()
        categ_serializer = CategorySerializer(category, many=True)
        return Response(categ_serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(["GET","PUT","DELETE"])
def categ_details_view(request,pk):
    category = get_object_or_404(Category,pk=pk)
    if request.method == "GET":
        categ_serializer = CategorySerializer(category)
        return Response(categ_serializer.data , status=status.HTTP_200_OK)
    elif request.method == "PUT":
        categ_serializer = CategorySerializer(category, data = request.data)
        # request.data mostly used with PUT and Patch method  means create new data if used with POSt else update in existing data
        if categ_serializer.is_valid(raise_exception=True):
            categ_serializer.save()
            return Response(categ_serializer.data , status=status.HTTP_200_OK)
    elif request.method=="DELETE":
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





