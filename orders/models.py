from django.db import models
from user_accounts.models import User
from menu.models import FoodIteam

# Create your models here.

class Payment(models.Model):
    PAYMENT_METHOD = (
        ('PayPal','PayPal'),
        ('Razorpay', 'RazorPay'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tarnsaction_id = models.CharField(max_length=100)
    payment_method = models.CharField(choices=PAYMENT_METHOD,max_length=100)
    amount = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tarnsaction_id
    
class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted', 'Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )

    user = models.ForeignKey(User , on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True,null=True)
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
    tax_data = models.JSONField(blank=True,help_text="Data format:{'tax_type' :{'tax_percentage':'tax_amount'}}")
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=20)
    status = models.CharField(max_length=15,choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    @property # this function act as field like compute in odoo combline two filed without saving in db
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.order_number
    
    


