from django.shortcuts import render, get_object_or_404
from .forms import Vendorform 
from user_accounts.forms import UserProfileForm
from user_accounts.models import UserProfile , User
from .models import Vendor


# Create your views here.
def vprofile(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    vendor = get_object_or_404(Vendor,user=request.user)


    vendor_form = Vendorform(instance=profile)
    profile_form = UserProfileForm(instance=vendor)
    context ={
        "v_form": vendor_form,
        "profile_form":profile_form
    }
    return render(request,'vendor/vprofile.html',context)
