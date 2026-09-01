import json

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from .models import User
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

from . import serializer
from .serializer import UserRegistrationSerializer, VendorRegistrationSerializer


@api_view(["POST", "GET"])
def registeruserapi(request):
    if request.method == "GET":
        users = User.objects.all()
        userserializer = UserRegistrationSerializer(users, many=True)
        return Response(userserializer.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def registervendorapi(request):

    data = {
        "user":json.loads(request.data['user']),
        "vendor_name": request.data['vendor_name'],
        "vendor_license":request.FILES.get('vendor_license')
    }
    print("DATA___",data)
    v_serializer = VendorRegistrationSerializer(data=data)
    if v_serializer.is_valid():
        v_serializer.save()
        return Response(v_serializer.data, status=status.HTTP_201_CREATED)
    print("Erros",v_serializer.errors)
    return Response(v_serializer.errors , status=status.HTTP_400_BAD_REQUEST)
