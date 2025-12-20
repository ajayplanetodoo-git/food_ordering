from django.shortcuts import render, get_object_or_404,redirect
from .forms import Vendorform
from menu.forms import Category_form
from user_accounts.forms import UserProfileForm
from user_accounts.models import UserProfile , User
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required , user_passes_test
from user_accounts.views import check_roles_vendor
from menu.models import Category ,FoodIteam
from django.template.defaultfilters import slugify


# Create your views here.
'''
this is help function insted of writting     vendor = Vendor.objects.get(user=request.user)
we make this help unction to get vendor
'''

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


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

@login_required(login_url='login')
@user_passes_test(check_roles_vendor)
def menu_builder(request):
    vendor = Vendor.objects.get(user=request.user)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request,'vendor/menu_builder.html',context)
@login_required(login_url='login')
@user_passes_test(check_roles_vendor)
def fooditeams_by_category(request,pk=None):
    vendor = get_vendor(request) # we can useed both     vendor = Vendor.objects.get(user=request.user)   or helper function get_vendor
    category = get_object_or_404(Category,pk=pk)
    print(vendor)
    fooditems = FoodIteam.objects.filter(vendor=vendor,category=category)
    print(category)
    print(fooditems)
    contxet = {
        'category':category,
        'fooditeam':fooditems
    }

    return render(request,'vendor/fooditeams_by_category.html',contxet)

def add_category(request,pk=None):
    vendor = get_vendor(request)
    print(vendor)
    if request.method=="POST":
        categ_from = Category_form(request.POST)
        if categ_from.is_valid():
            category_name=categ_from.cleaned_data['category_name']
            category = categ_from.save(commit=False)
            category.vendor=vendor
            category.slug = slugify(category_name)
            categ_from.save()
            messages.success(request,"Category added ")
            return redirect('menubuilder')
        else:
            print(messages.error)
    else:
        categ_from = Category_form()
    context={
        "form":categ_from,
    }
    return render(request,'vendor/add_category.html',context)



def edit_category(request,pk=None):
    vendor = Vendor.objects.get(user=request.user)
    category = get_object_or_404(Category,pk=pk)
    print(vendor)
    print(category)
    if request.method=="POST":
        categ_from = Category_form(request.POST,instance=category)
        if categ_from.is_valid():
            category_name=categ_from.cleaned_data['category_name']
            category = categ_from.save(commit=False)
            category.vendor=vendor
            category.slug = slugify(category_name)
            categ_from.save()
            messages.success(request,"Category Updated ")
            return redirect('menubuilder')
        else:
            print(messages.error)
    else:
        categ_from = Category_form(instance=category)
    context={
        "form":categ_from,
        'category':category,
    }
    
    return render(request,'vendor/edit_category.html',context)


def delete_category(request,pk=None):
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request," The category is delete successfully")
    return redirect('menubuilder')


