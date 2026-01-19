from django.shortcuts import render , redirect
from marketplace.models import Cart
from user_accounts.models import UserProfile
from marketplace.context_processors import get_cart_total

from orders.forms import OrderForm


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
            pass
        else:
            print(form.error)



    return render(request, 'orders/place_order.html')