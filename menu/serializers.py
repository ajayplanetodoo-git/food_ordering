from rest_framework import serializers
from .models import FoodIteam , Category

'''
1. Category API - Done
2. Food Items API - Done
3. Menu API
4. User Registration-Done
5. Vendor Registration-Done
6. JWT Authentication
7. Permissions
8. Cart API
9. Order API
10. Payment API
11. Chatbot APIs
12. OpenAI/Gemini
'''

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta :
        model = FoodIteam
        fields =['id','food_title','description','price','image','is_available']

class CategorySerializer(serializers.ModelSerializer):
    fooditeams = FoodItemSerializer(many=True,read_only=True)
    class Meta:
        model = Category
        fields = ['id','category_name','description','fooditeams']
#
class MenuSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = FoodIteam
        fields = ['vendor','category','food_title','description','price','image','is_available']