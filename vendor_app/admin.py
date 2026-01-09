from django.contrib import admin
from .models import Vendor , OpeningHour
# Register your models here.

class vendoradmin(admin.ModelAdmin):
    list_display =("user","vendor_name",'is_approved','created_at')
    list_display_links = ('user',"vendor_name")

class OpeningHoursAdmin(admin.ModelAdmin):
    list_display = ('vendor','day','from_hour','to_hour')

admin.site.register(Vendor,vendoradmin)
admin.site.register(OpeningHour,OpeningHoursAdmin)
