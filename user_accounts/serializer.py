from typing import Any

from rest_framework import serializers
# from rest_framework.serializers import _MT

from .models import User ,UserProfile
from vendor_app.models import Vendor



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password','phone_number','role']

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'],
                                        email=validated_data['email'],
                                        password=validated_data['password'])
        user.role = User.CUSTOMER
        user.save()
        return user

class VendorRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()
    class Meta:
        model = Vendor
        fields = ['user','vendor_name','vendor_license']
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['user']['username'],
                                        first_name=validated_data['user']['first_name'],
                                        last_name=validated_data['user']['last_name'],
                                        email=validated_data['user']['email'],
                                        password=validated_data['user']['password'])

        user_profile = UserProfile.objects.create(
            user=user
        )

        vendor = Vendor.objects.create(
            user = user,
            user_profile = user_profile,
            vendor_name = validated_data['vendor_name'],
            vendor_license = validated_data['vendor_license']
        )
        user.role = User.VENDOR
        vendor.save()
        return vendor


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture','cover_picture','address','country','state','city','pincode']

