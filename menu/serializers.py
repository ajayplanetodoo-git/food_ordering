from rest_framework import serializers
from .models import FoodIteam , Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class FoodItemSerializer(serializers.ModelSerializer):
    fooditeams = CategorySerializer(many=True, read_only=True)
    class Meta :
        model = FoodIteam
        fields = '__all__'
