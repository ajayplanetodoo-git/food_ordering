from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import Userform
from vendor_app.forms import Vendorform
from .models import User , UserProfile
from django.contrib import messages , auth
from .utils import detectuser
from django.contrib.auth.decorators import login_required

# Create your views here.
def registeruser(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already looged in!")
        return redirect("myaccount")
    elif request.method=="POST":
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
            messages.success(request,"You account has been registered succesfully")  #  here we are use django messeges 
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


def registervendor(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already looged in!")
        return redirect("myaccount")
    elif request.method == 'POST':
        user_form = Userform(request.POST)
        ven_form = Vendorform(request.POST,request.FILES)
        if user_form.is_valid() and ven_form.is_valid():
            firstname = user_form.cleaned_data.get("first_name")
            lastname = user_form.cleaned_data.get("last_name")
            username = user_form.cleaned_data.get("username")
            email = user_form.cleaned_data.get('email')
            password = user_form.cleaned_data.get('password')
            user = User.objects.create_user(
                first_name=firstname,
                last_name=lastname,
                username=username,
                email=email,
                password=password
            )
            user.role = User.VENDOR
            user.save()

#  Get profile created by signal
            user_profile = UserProfile.objects.get(user=user)
#   create vendor
            vendor = ven_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request,"Your Account Registartion Succesfully! please wait for approval ")
            return redirect("vendorregister")  # when anywhere we used any django messages.success the we have to redircet is complusery esle it not work propwely

        else:
            print("form is invalid")
            print(user_form.errors)
    else:
        user_form = Userform()
        ven_form = Vendorform()


    conatext ={
        "u_form": user_form,
        "v_form": ven_form,
    }
    return render(request,"user_accounts/vendor_registration.html",conatext)



def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already looged in!")
        return redirect("myaccount")
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=email,password=password)   # here we areathenticate it take two paramaerts  from  email couse in user model we used 
                                                                    # USERNAME_FIELD = 'email' so 
        
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You are logged in ")
            return redirect('myaccount')
        else:
            messages.error(request,"Invalid login credentials")
            return redirect("login")
        
    return render(request, 'user_accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out")
    return redirect('login')

@login_required(login_url='login') # this is 
def myaccount(request):
    user = request.user
    redirectUrl = detectuser(user)  # here the use of helper function from util.py
    return redirect(redirectUrl)

@login_required(login_url='login')
def custmerdashboard(request):
    return render(request,"user_accounts/custdashboard.html")

@login_required(login_url='login')
def vendordashboard(request):
    return render(request,"user_accounts/vendashboard.html")