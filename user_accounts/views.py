from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import Userform
from .models import User
from django.contrib import messages

# Create your views here.
def registeruser(request):
    if request.method=="POST":
        print(request.POST)
        form = Userform(request.POST)
        if form.is_valid():
            # create the user using the form
            # password = user.cleaned_data["password"]
            # user = form.save(commit=False) # here are form are ready to save grab all data 
            # user.set_password(password) # here hassing the pasword
            # user.role = User.CUSTOMER # here is we are assinged user role
            # user.save()

            # create the user using create_user mathod
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
                )
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,"You account has been registered succesfully")
            print("User is created")
            return redirect("userregister")
        else:
            print(form.errors)
    else:
        form = Userform()
    context = {
        "forms" : form,
    }
    return render(request,"user_accounts/registration.html",context)

