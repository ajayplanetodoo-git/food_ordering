from django.shortcuts import render, redirect, get_object_or_404 
from vendor_app.models import Vendor
from menu.models import Category, FoodIteam
from django.db.models import Prefetch
from django.http import HttpResponse , JsonResponse
from marketplace.models import Cart
from .context_processors import get_cart_counter
from django.contrib.auth.decorators import login_required , user_passes_test


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

    if request.user.is_authenticated:
        cart_iteams = Cart.objects.filter(user=request.user)
    else:
        cart_iteams = Cart.objects.none() 
    context = {
        'vendor':vendor,
        'category': categoy,
        'cart_iteams' : cart_iteams,
    }
    return render(request,'marketplace/vendor_details.html',context)

def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the food iteam exists
            try:
                fooditeam = FoodIteam.objects.get(id=food_id)
                # check if user already added that food to cart
                try: 
                    chkcart = Cart.objects.get(user=request.user , fooditeam=fooditeam)
                    # increase cart quntity
                    chkcart.quantity+=1
                    chkcart.save()
                    return JsonResponse({"status":'Success','message':'Increased the cart quanitiy',
                                         'cart_counter':get_cart_counter(request),'qty':chkcart.quantity,'food_id':food_id})
                except :
                    chkcart = Cart.objects.create(user=request.user , fooditeam=fooditeam, quantity=1)
                    return JsonResponse({'status':'success','message':"Added the food to cart",
                                         'cart_counter':get_cart_counter(request),'qty':chkcart.quantity,'food_id':food_id})
            except:
                return JsonResponse({'failed':'success','message':'This food doesnot exist'})
        else:        
            return JsonResponse({'status':'failed','message':'invalid request'})
    else:
        return  JsonResponse({'status':'failed','message':'Please login to continue'})


def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check if the food iteam exists
            try:
                fooditeam = FoodIteam.objects.get(id=food_id)
                # check if user already added that food to cart
                try: 
                    chkcart = Cart.objects.get(user=request.user , fooditeam=fooditeam)
                    if chkcart.quantity >  1:
                        # Decrease Qty cart quntity
                        chkcart.quantity-=1
                        chkcart.save()
                    else:
                        chkcart.delete()
                        chkcart.quantity = 0
                    return JsonResponse({"status":'Success',
                                         'cart_counter':get_cart_counter(request),'qty':chkcart.quantity,'food_id':food_id})
                except :
                    return JsonResponse({'status':'Failure','message':"You do not have this item in your cart!" ,'cart_counter':get_cart_counter(request)
                                        })
            except:
                return JsonResponse({'status':'success','message':'This food doesnot exist'})
        else:        
            return JsonResponse({'status':'failed','message':'invalid request'})
    else:
        return  JsonResponse({'status':'failed','message':'Please login to continue'})


@login_required(login_url='login')
def cart(request):
    cart_iteams = Cart.objects.filter(user=request.user).order_by('updated_at')
    # sub_total=0
    # for rec in cart_iteams:
    #     price = rec.quantity* rec.fooditeam.price
    #     sub_total+=price

    context = {
        'cart':cart_iteams,
        # 'total':sub_total,
    }
    return render(request , 'marketplace/cart.html',context)


def delete_cart(request,cart_id):
     if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                #Check if the item exists
                cart_iteam = Cart.objects.get(user=request.user, id=cart_id)
                if cart_iteam:
                    cart_iteam.delete()
                    return JsonResponse({'status':'success','message':'Cart item has been deleted!', 
                                         'cart_counter':{'cart_count':get_cart_counter(request)}
                                         
                                         })
            except:
                return JsonResponse({'status':'success','message':'This cart doesnot exist'})

        else:
            return JsonResponse({'status':'failed','message':'invalid request'})

