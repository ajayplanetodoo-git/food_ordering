from django.shortcuts import render , redirect
from django.http import HttpResponse

# Create your views here.
def registeruser(request):
    return HttpResponse("This is my user registration form")