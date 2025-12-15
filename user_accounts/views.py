from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import Userform
from vendor_app.forms import Vendorform
from .models import User , UserProfile 
from vendor_app.models import Vendor
from django.contrib import messages , auth
from .utils import detectuser , send_varification_link 
from django.contrib.auth.decorators import login_required , user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


# Create your views here.


def registeruser(request):
    if request.user.is_authenticated: # if user have allready loin it not accce again login pg thsi is authentication
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
            #  send verification email
            mail_subject = "activate your account"
            mail_template = 'user_accounts/emails/account_verfy_email.html'
            send_varification_link(request,user,mail_subject,mail_template)
            messages.success(request,"You account has been registered succesfully")  #  here we are use django messeges 
            print("User is created")
            return redirect("login")
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
            
#   create vendor
            vendor = ven_form.save(commit=False)
            vendor.user = user
            #  Get profile created by signal
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            #  send verification email`
            mail_subject = "activate your account"
            mail_template = 'user_accounts/emails/account_verfy_email.html'
            send_varification_link(request,user,mail_subject,mail_template)



            messages.success(request,"Your Account Registartion Succesfully! please wait for approval ")
            return redirect("login")  # when anywhere we used any django messages.success the we have to redircet is complusery esle it not work propwely

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


def activate(request,uiddb64, token):
    #activate the user by setting the is_active status true  after clicking on email link
    try:
        uid= urlsafe_base64_decode(uiddb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError):
        user = None

    if user is not None and  default_token_generator.check_token(user,token):
        user.is_active =True
        user.save()
        messages.success(request,"Congratulation! Your user is active")
        return redirect("myaccount")
    else:
        messages.error(request,"Invalid activation link")
        return redirect('myaccount')

    return
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


# Restrict vendor from accesing customer page
def check_roles_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Restrict customer from accesing vendor page
def check_roles_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

'''
this  function is used for  detect which  redirect to util.py function detectuser()  ,
kind of user id  tha  vendor, customer or any thing then i will redicret to accordingly 
if user is vendor it will redirect to vendordashboard or customerdashboard urls and page
'''

@login_required(login_url='login') # this is  decorater used for rectrictions 
def myaccount(request):
    user = request.user
    redirectUrl = detectuser(user)  # here the use of helper function from util.py  detect user to check which kind of user is
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_roles_customer)
def custmerdashboard(request):
    user = request.user
    print(user)
    context = {
        'user':user
    }
    return render(request,"user_accounts/custdashboard.html",context)

@login_required(login_url='login')
@user_passes_test(check_roles_vendor)
def vendordashboard(request):
    return render(request,"user_accounts/vendashboard.html")

def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out")
    return redirect('login')

def forgot_password(request):
    if request.method =="POST":
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            #send reset password 
            mail_subject = "Reset Your Password"
            mail_template = 'user_accounts/emails/reset_password_email.html'
            send_varification_link(request,user,mail_subject,mail_template)
            messages.success(request,"Password reset email has been send on your email")
            return redirect("login")
        else:
            messages.error(request,"Account doesnot exist")
            return redirect("forgot_password")
    return render(request,'user_accounts/forgot_password.html')


def reset_password_validate(request,uiddb64,token):
    # validating the user by decoding the   token and user.pk
    try:
        uid= urlsafe_base64_decode(uiddb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError):
        user = None

    if user is not None and  default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.info(request,"Please reset your password")
        return redirect('reset_password')
    else:
        messages.error(request,'This link hase be expired')
        return redirect('myaccount')

def reset_password(request):    
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request,"Password is succesfully change")
            return redirect('login')

        else:
            messages.error("Pasword is not matched")
            return redirect('reset_password')
    return render(request,'user_accounts/reset_password.html')


