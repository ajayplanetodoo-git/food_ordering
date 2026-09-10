import json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from .models import User
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from .serializer import UserRegistrationSerializer, VendorRegistrationSerializer, LoginSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


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
        "user": json.loads(request.data['user']),
        "vendor_name": request.data['vendor_name'],
        "vendor_license": request.FILES.get('vendor_license')
    }
    print("DATA___", data)
    v_serializer = VendorRegistrationSerializer(data=data)
    if v_serializer.is_valid():
        v_serializer.save()
        return Response(v_serializer.data, status=status.HTTP_201_CREATED)
    print("Erros", v_serializer.errors)
    return Response(v_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        check_user = get_object_or_404(User, email=email)
        if check_user.is_active == False:
            return Response({"error": " account not active please check mail and activate "},
                status=status.HTTP_401_UNAUTHORIZED
            )
        user = authenticate(username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserRegistrationSerializer(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": user_serializer.data
            })