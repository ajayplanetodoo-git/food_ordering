from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view ,parser_classes
from .models import Category, FoodIteam
from .serializers import CategorySerializer, FoodItemSerializer
from rest_framework.parsers import MultiPartParser,FormParser ,FileUploadParser
from  django.template.defaultfilters import slugify


#  this api endpoint is only for CURD of category app
@api_view(["GET", "POST" ])
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



# this is api end point for FoodItems .
# in this function we can add new and fetch food items
@api_view(["GET","POST"])
def food_item_view(request):
    food_item = FoodIteam.objects.all()
    if request.method == 'GET': # get only for fetching data
        food_serializer = FoodItemSerializer(food_item,many=True)
        return Response(food_serializer.data,status=status.HTTP_200_OK)
    elif request.method == "POST": # from Post method we can add food through api
        serializer = FoodItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            food = serializer.save()
            food_name = food.food_title
            food.slug = slugify(food_name) + '-' + str(food.id)
            food.is_available = True
            food.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)


# in this function we fetch by id and also we can update that record using pk
@api_view(["GET","PUT"])
@parser_classes([MultiPartParser,FormParser])
def food_item_details(request,pk):
    food_item = get_object_or_404(FoodIteam,pk=pk)
    if request.method == "GET":
        food_serilizer = FoodItemSerializer(food_item)
        return Response(food_serilizer.data, status=status.HTTP_200_OK)
    if request.method == "PUT": # this for upadte in existing record we sholud pass id
        food_serilizer = FoodItemSerializer(food_item,data = request.data)

        if food_serilizer.is_valid(raise_exception=True):
            food = food_serilizer.save()
            food_name = food.food_title
            food.slug = slugify(food_name) +'-'+ str(food.id)
            food.is_available = True
            food.save()
            return Response (food_serilizer.data,status=status.HTTP_200_OK)






