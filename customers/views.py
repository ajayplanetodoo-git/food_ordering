from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from user_accounts.forms import  UserProfileForm ,UserInfoForm
from user_accounts.models import User,UserProfile
from django.contrib import messages 

# Create your views here.

@login_required(login_url='login')
def cust_profile(request):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    if request.method == "POST":
        u_form = UserInfoForm(request.POST,instance=user)
        u_profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        if u_form.is_valid() and u_profile_form.is_valid():
            u_form.save()
            u_profile_form.save()
            messages.success(request,"Profile is Updated successfully")
            return redirect('customer_profile')
    else:
        u_form = UserInfoForm(instance=user)
        u_profile_form = UserProfileForm(instance=profile)
    context ={
        'u_info_form' : u_form, 
        'u_profile_form' : u_profile_form,
        'profile' : profile,

    }
    return render(request,'customers/cust_profile.html',context)