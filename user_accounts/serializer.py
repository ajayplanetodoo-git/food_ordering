from rest_framework import serializers
from .models import User ,UserProfile



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','phone_number','role']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture','cover_picture','address','country','state','city','pincode']

