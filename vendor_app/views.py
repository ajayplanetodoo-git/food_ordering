from django.shortcuts import render, get_object_or_404,redirect
from .forms import Vendorform
from menu.forms import Category_form ,FoodIteam_form
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
'''
category Curd opertaions
'''
@login_required(login_url='login')
@user_passes_test(check_roles_vendor)
def add_category(request):
    vendor = get_vendor(request)
    print(vendor)
    if request.method=="POST":
        categ_from = Category_form(request.POST)
        if categ_from.is_valid():
            category_name=categ_from.cleaned_data['category_name']
            category = categ_from.save(commit=False)
            category.vendor=vendor
            category.save() # here the cateogry id will be genrated 
            category.slug = slugify(category_name)+'-'+str(category.id) # chickrn-15
            category.save()
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


@login_required(login_url='login')
@user_passes_test(check_roles_vendor)
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

@login_required(login_url='login')
@user_passes_test(check_roles_vendor)
def delete_category(request,pk=None):
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request," The category is delete successfully")
    return redirect('menubuilder')


'''
Fooditeams curd operations
'''
@login_required(login_url='login')
@user_passes_test(check_roles_vendor)
def add_fooditeam(request):
    vendor=get_vendor(request)
    if request.method=="POST":
        fooditeam_form = FoodIteam_form(request.POST,request.FILES)
        if fooditeam_form.is_valid():
            foodtitle=fooditeam_form.cleaned_data['food_title']
            food = fooditeam_form.save(commit=False)
            food.vendor=vendor
            food.slug = slugify(foodtitle)
            food.save()
            messages.success(request,"FoodItem added ")
            return redirect('fooditems_by_category',food.category.id)
        else:
            print(fooditeam_form.errors)
    else:
        fooditeam_form = FoodIteam_form()
        # modify this form 
        fooditeam_form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'foodform':fooditeam_form
    }

    return render(request,'vendor/add_fooditeam.html',context)

@login_required(login_url='login')
@user_passes_test(check_roles_vendor)
def edit_fooditeam(request,pk=None):
    vendor = Vendor.objects.get(user=request.user)
    food = get_object_or_404(FoodIteam,pk=pk,vendor=vendor)
    print(vendor)
    print(food)
    if request.method=="POST":
        food_from = FoodIteam_form(request.POST,request.FILES,instance=food)
        if food_from.is_valid():
            food_title=food_from.cleaned_data['food_title']
            food = food_from.save(commit=False)
            food.vendor=vendor
            food.slug = slugify(food_title)
            food.save()
            messages.success(request,"Food Iteam Updated ")
            return redirect('fooditems_by_category',food.category.id)
        else:
            print(messages.error)
    else:
        food_from = FoodIteam_form(instance=food)
        food_from.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))

    context={
        "foodform":food_from,
        'food':food,
    }
    
    return render(request,'vendor/edit_fooditeam.html',context)

@login_required(login_url='login')
@user_passes_test(check_roles_vendor)
def delete_fooditeam(request,pk=None):
    food = get_object_or_404(FoodIteam,pk=pk)
    food.delete()
    messages.success(request," The category is delete successfully")
    return redirect('fooditems_by_category',food.category.id)