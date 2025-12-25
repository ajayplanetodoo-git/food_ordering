from django.shortcuts import render, redirect, get_object_or_404 
from vendor_app.models import Vendor
from menu.models import Category, FoodIteam
from django.db.models import Prefetch
from django.http import HttpResponse

def marketplace(request):
    vendor = Vendor.objects.filter(is_approved=True,user__is_active=True)[:8]
    vendor_count = vendor.count()
    context = {
        'vendors':vendor,
        'vendor_count' : vendor_count,
    }

    return render(request,'marketplace/listing.html',context)


def vendor_details(request,vendor_slug):
    vendor = get_object_or_404(Vendor,vendor_slug=vendor_slug)
    categoy = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditeams',
            queryset=FoodIteam.objects.filter(is_available=True)
        )
    )
    context = {
        'vendor':vendor,
        'category': categoy,
    }
    return render(request,'marketplace/vendor_details.html',context)

def add_to_cart(request,food_id):
    return  HttpResponse(food_id)

