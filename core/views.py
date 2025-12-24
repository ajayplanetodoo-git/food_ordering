from django.shortcuts import render , redirect
from django.http import HttpResponse

from vendor_app.models import Vendor
def home(request):
    vendor = Vendor.objects.filter(is_approved=True,user__is_active=True)[:8]
    context = {
        'vendors':vendor,
    }
    return render(request,"home.html",context)