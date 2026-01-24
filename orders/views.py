from django.http import HttpRequest,HttpResponse , JsonResponse
from django.shortcuts import render , redirect
from marketplace.models import Cart
from user_accounts.models import UserProfile
from marketplace.context_processors import get_cart_total

from orders.forms import OrderForm
from .models import Order
import simplejson as json
from .utils import generate_order_number
from .models import Order , Payment ,OrderedFood

from user_accounts .utils import send_notification
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
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

@login_required(login_url='login')
def payment(request):
    # check request is ajxa or not 
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method=='POST':
        # Store payment details in the payment model
        order_no = request.POST.get("order_no")
        transcation_id = request.POST.get('transcation_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status')

        order = Order.objects.get(user=request.user , order_no = order_no)
        payment =  Payment(
            user = request.user,
            transcation_id = transcation_id,
            payment_method = payment_method,
            amount = order.total,
            status = status
        )
        payment.save()

    # Update the order  model
    order.payment = payment
    order.is_ordered = True
    order.save()


    #Move tha cart items to ordered food model
    cart_iteam = Cart.objects.filter(user = request.user)
    for item in cart_iteam:
        ordered_food = OrderedFood()
        ordered_food.order = order
        ordered_food.payment = payment
        ordered_food.user = request.user
        ordered_food.food_items = item.fooditeam
        ordered_food.qunatity = item.quantity
        ordered_food.price = item.fooditeam.price
        ordered_food.amount = item.quantity * item.fooditeam.price
        ordered_food.save()
    
   


    #send order confirmation mail to customer
    mail_subject = "Thanku you for Ordering with us"
    mail_template = 'orders/order_confirmation_email.html'

    context =  {
        'user':request.user,
        'order' : order,
        'to_email': order.email,

    }

    send_notification(mail_subject,mail_template,context)


    # send order recievd mail to the vendor  imp thing is here  vvendor may be multipal
    mail_subject = 'You have recived new order'
    mail_template = 'order/new_order_recived.html'
    to_emails = []
    for i in cart_iteam:
        if i.fooditeam.vendor.user.email not in to_emails:
            to_emails.append(i.fooditeam.vendor.user.email)
    print('to_emails==>',to_emails)
    context = {
        'order' : order,
        'to_emails' : to_emails,
    }
    send_notification(mail_subject,mail_template,context)


    # clear the cart if the payment is success 
    cart_iteam.delete()
    #  return back to ajax with status succse or fauiler
    response =  {
        'order_no' : order_no,
        'transcation_id' : transcation_id

    }
    return JsonResponse(response)


def order_complete(request):
    return render(request,'orders/order_complete.html')
