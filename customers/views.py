from django.shortcuts import render , get_object_or_404 , redirect
from django.contrib.auth.decorators import login_required
from user_accounts.forms import  UserProfileForm ,UserInfoForm
from user_accounts.models import User,UserProfile
from django.contrib import messages
from orders.models import Order , OrderedFood

import simplejson as json

# Create your views here.

@login_required(login_url='login')
def cust_profile(request):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    if request.method == "POST":
        u_form = UserInfoForm(request.POST,instance=user)
        u_profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        if u_form.is_valid() and u_profOrderedFoodile_form.is_valid():
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


def my_orders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context = {
        'my_orders':orders,
    }
    return render(request,'customers/my_orders.html',context)


def order_details(request,order_no):
    try :
        order = Order.objects.get(order_no=order_no,is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food:
            subtotal+= (item.price*item.qunatity)
        tax_data = json.loads(order.tax_data)
        contexet = {
            'order' : order,
            'ordered_food' : ordered_food,
            'subtotal':subtotal,
            'tax_data' : tax_data,
        }
        return render(request ,'customers/order_details.html',contexet)

    except :
        return redirect ('customer')
