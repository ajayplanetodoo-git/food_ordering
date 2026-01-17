from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user_accounts.forms import  UserProfileForm ,UserInfoForm
from user_accounts.models import User,UserProfile
# Create your views here.

@login_required(login_url='login')
def cust_profile(request,pk=None):
    user_info = User.objects.get(pk=request.user.pk)
    u_info_form = UserInfoForm(instance=user_info)
    u_profile_form = UserProfileForm()
    context ={
        'u_info_form' : u_info_form,
        'u_profile_form' : u_profile_form,
    }
    return render(request,'customers/cust_profile.html',context)