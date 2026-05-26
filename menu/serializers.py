from rest_framework import serializers
from .models import FoodIteam , Category

#
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = "__all__"

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta :
        model = FoodIteam
        fields =['id','food_title','vendor','category','description','price','image','is_available']

class CategorySerializer(serializers.ModelSerializer):
    fooditeams = FoodItemSerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ['id','category_name','description','fooditeams']
