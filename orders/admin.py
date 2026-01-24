from django.contrib import admin
from .models import Payment,Order,OrderedFood
# Register your models here.

#  this class responsible for showing which fooditeam belong to which oredr no show we used Tablularinline
class OrderedFoodinLine(admin.TabularInline): 
    model = OrderedFood
    readonly_fields = ('order','payment','user','food_items','qunatity','price','amount')
    extra = 0 # this used becouse we  dont need extra filed in tabler table 

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_no','name','phone','email','total','payment_method','status','is_ordered']
    inlines = [OrderedFood]

admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderedFood)

