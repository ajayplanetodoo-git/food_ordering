from .models import Cart
from menu.models import FoodIteam

def get_cart_counter(request):
    cart_count=0
    if request.user.is_authenticated:
        try:
            cart_iteams = Cart.objects.filter(user=request.user)
            if cart_iteams:
                for cart_item in cart_iteams:
                    cart_count+=cart_item.quantity
            else:
                cart_count=0
        except:
            cart_count=0
    return dict(cart_count=cart_count)

def get_cart_total(request):
    subtotal=0
    tax=0
    grand_total=0
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(user=request.user)
        for itm in cart_item:
            price = itm.quantity * itm.fooditeam.price
            subtotal += price
        grand_total=subtotal+tax
    return dict(subtotal=subtotal,tax=tax, grand_total=grand_total)