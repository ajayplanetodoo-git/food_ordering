from django.http import HttpRequest,HttpResponse
from django.shortcuts import render , redirect
from marketplace.models import Cart
from user_accounts.models import UserProfile
from marketplace.context_processors import get_cart_total

from orders.forms import OrderForm
from .models import Order
import simplejson as json
from .utils import generate_order_number

# Create your views here.

def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if cart_count <=0:
        return redirect('marketplace')
    
    subtotal = get_cart_total(request)['subtotal']
    total_tax = get_cart_total(request)['tax']    
    grand_total = get_cart_total(request)['grand_total']
    tax_data = get_cart_total(request)['tax_dict']
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']  # this is the input id of  html radio button of razorpay & paypal 
            order.save() # here order will save and pk will generate 
            order.order_no = generate_order_number(order.id)
            order.save()
            context = {
                "order":order,
                'cart_item' : cart_items,
            }
            return render(request, 'orders/place_order.html',context)
        else:
            print(form.error)
    return render(request, 'orders/place_order.html')

def payment(request):
    pass