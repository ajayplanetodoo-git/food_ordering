from django.shortcuts import render, redirect, get_object_or_404 
from vendor_app.models import Vendor , OpeningHour
from menu.models import Category, FoodIteam
from django.db.models import Prefetch
from django.http import HttpResponse , JsonResponse
from marketplace.models import Cart
from .context_processors import get_cart_counter
from django.contrib.auth.decorators import login_required , user_passes_test
from django.db.models import Q
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D # ``D`` is a shortcut for ``Distance``
from django.contrib.gis.db.models.functions import Distance
from datetime import date , datetime
from django.utils import timezone
from orders.forms import OrderForm
from user_accounts.models import UserProfile
import pytz

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
#    Current Opeing Hours cxalculation
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day','-from_hour')
    
    today_date = date.today()
    day= today_date.isoweekday()
    current_opening_hours = OpeningHour.objects.filter(vendor=vendor,day=day)

    

    if request.user.is_authenticated:
        cart_iteams = Cart.objects.filter(user=request.user)
    else:
        cart_iteams = Cart.objects.none() 
    context = {
        'vendor':vendor,
        'category': categoy,
        'cart_iteams' : cart_iteams,
        'opening_hours' : opening_hours,
        'current_opeing_hr' : current_opening_hours,
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
    
def search(request):
    if not 'address' in request.GET:
        return redirect('marketplace')
    else:
        address = request.GET['address']
        latitude = request.GET['lat']
        longitude = request.GET['lng']
        radius = request.GET['radius']
        keyword = request.GET['keyword']
    # get vendor id that has the food item that user looking
        fetch_vedor_by_fooditem= FoodIteam.objects.filter(food_title__icontains=keyword,
                                                        is_available=True).values_list('vendor',flat=True) # value_list used of it return id and 'vendor 
        # must br pesent in fooditeams flat=true give you simple list like [1,2,3]  
        vendor = Vendor.objects.filter(Q(id__in=fetch_vedor_by_fooditem) |  
                                    Q(vendor_name__icontains=keyword,is_approved=True))

        if latitude and longitude and radius:
            pnt = GEOSGeometry("POINT(%s %s)" % (longitude,latitude))

            vendor = Vendor.objects.filter(Q(id__in=fetch_vedor_by_fooditem) |  
                                    Q(vendor_name__icontains=keyword,is_approved=True),
                                    user_profile__location__distance_lte=(pnt, D(km=radius))
                                    ).annotate(distance_u=Distance('user_profile__location',pnt)).order_by('distance_u')
                                    #    distance_u id used difine in annotate 
            
            for v in vendor:
                v.kms = round(v.distance_u.km,1)

        vendor_count = vendor.count()
        context ={
            'vendors' : vendor,
            'vendor_count':vendor_count,
            'source_location': address,
        }

        return render(request , 'marketplace/listing.html',context)
    
@login_required(login_url='login')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if cart_count <=0:
        return redirect('marketplace')

    default_value = {
        'first_name':user.first_name,
        'last_name':user.last_name,
        'email':user.email,
        'phone' : user.phone_number,
        'address': user_profile.address,
        'country':user_profile.country,
        'state':user_profile.state,
        'city':user_profile.city,
        'pin_code' : user_profile.pincode,
    }
    order_forms = OrderForm(initial=default_value)  # using inital we can propulate data from from model to form like profile model data prepoluated in orderforms
                                                     # if used . save we aslo save data in oredr model

    context = {
        'form':order_forms,
        'cart' : cart_items
    }
    return render(request, 'marketplace/checkout.html',context)
