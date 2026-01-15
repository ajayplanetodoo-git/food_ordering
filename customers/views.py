from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user_accounts.forms import  UserProfileForm ,UserInfoForm
# Create your views here.

@login_required(login_url='login')
def cust_profile(request):
    u_profile_form = UserProfileForm()
    context ={
        'u_info_form' : UserInfoForm, 
        'u_profile_form' : u_profile_form,
    }
    return render(request,'customers/cust_profile.html',context)