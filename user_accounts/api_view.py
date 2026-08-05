from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes

from . import serializer
from .serializer import UserRegistrationSerializer

@api_view(["POST"])
def regisetuserapi(request):
    if request.method == "POST":
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid( raise_exception=True):
            serializer.save()

