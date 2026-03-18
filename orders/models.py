from django.db import models
from user_accounts.models import User
from menu.models import FoodIteam
from vendor_app.models import Vendor
import simplejson as json
request_object = ""
# Create your models here.

class Payment(models.Model):
    PAYMENT_METHOD = (
        ('PayPal','PayPal'),
        ('Razorpay', 'RazorPay'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD,max_length=100)
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id
    
class Order(models.Model):

    
    STATUS = (
        ('New','New'),
        ('Accepted', 'Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )

    user = models.ForeignKey(User , on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True,null=True)
    vendor = models.ManyToManyField(Vendor,blank=True)
    order_no = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=100,blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=200)
    country = models.CharField(max_length=15,blank=True)
    state = models.CharField(max_length=15,blank=True)
    city = models.CharField(max_length=50)
    pin_code =models.CharField(max_length=10)
    total = models.FloatField()
    tax_data = models.JSONField(blank=True,help_text="Data format:{'tax_type' :{'tax_percentage':'tax_amount'}}",null=True)
    total_data = models.JSONField(blank=True,null=True)
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=20)
    status = models.CharField(max_length=15,choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property # this function act as field like compute in odoo combline two filed without saving in db
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    def order_place_to(self):
        return ",".join([str(i) for i in self.vendor.all()])
    

    # this function used for vender details order how may order vendor got and according to that calculate monthaly revanu
    def get_total_byvendor(self):
        vendor = Vendor.objects.get(user=request_object.user)
        subtotal =0
        tax =0
        tax_dict = {}
        if self.total_data:
            total_data = json.loads(self.total_data)
            data = total_data.get(str(vendor.id))

            
            for key,val in data.items():
                subtotal += float(key)
                val = val.replace("'",'"')
                val = json.loads(val)
                tax_dict.update(val)
                #  calculate Tax
                # {'CGST':{'9.00':'6.01'},'SGST':{'7.00':'4.60'}}
                for i in val:
                    for j in val[i]:
                        tax += float(val[i][j])
        garnd_total = float((subtotal)+float(tax))
        
        context = {
            'subtotal':subtotal,
            'tax':tax,
            'tax_dict':tax_dict,
            'grand_total' :garnd_total,

        }


            
        return context
    
    def __str__(self):
        return self.order_no
    
class OrderedFood(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    food_items = models.ForeignKey(FoodIteam, on_delete=models.CASCADE)

    qunatity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.food_items.food_title

    


