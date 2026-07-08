from rest_framework import serializers
from .models import User ,UserProfile



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password','phone_number','role']

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'],
                                        phone_number = validated_data['phone_number'],
                                        role=validated_data['role'],
                                        email=validated_data['email'],
                                        password=validated_data['password'])

        return user
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture','cover_picture','address','country','state','city','pincode']

