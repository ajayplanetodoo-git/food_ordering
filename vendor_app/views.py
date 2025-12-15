from django.shortcuts import render, get_object_or_404,redirect
from .forms import Vendorform 
from user_accounts.forms import UserProfileForm
from user_accounts.models import UserProfile , User
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required , user_passes_test
from user_accounts.views import check_roles_vendor


# Create your views here.

@login_required(login_url='login')
@user_passes_test(check_roles_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    vendor = get_object_or_404(Vendor,user=request.user)
    
    if request.method=="POST":
        vendor_form = Vendorform(request.POST,request.FILES,instance=vendor)
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        if vendor_form.is_valid() and profile_form.is_valid():
            vendor_form.save()
            profile_form.save()
            messages.success(request,"Profile is upadte successfully")
            return redirect('vprofile')
        else:
            print(vendor_form.errors)
            print(profile_form.errors)

    else:
        vendor_form = Vendorform(instance=vendor)
        profile_form = UserProfileForm(instance=profile)

    context ={
        "v_form": vendor_form,
        "profile_form":profile_form,
        "profile" : profile,
        "vendor" : vendor
    }
    return render(request,'vendor/vprofile.html',context)
