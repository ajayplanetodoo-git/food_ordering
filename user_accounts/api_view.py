from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from .models import User

from . import serializer
from .serializer import UserRegistrationSerializer

@api_view(["POST","GET"])
def registeruserapi(request):
    if request.method == "GET":
        users= User.objects.all()
        userserializer =  UserRegistrationSerializer(users, many=True)
        return Response(userserializer.data , status=status.HTTP_200_OK)
    if request.method == "POST":
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid( raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

