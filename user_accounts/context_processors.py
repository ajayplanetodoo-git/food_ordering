
from vendor_app.models import Vendor
from django.conf import settings

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor=None
    return dict(vendor=vendor)

'''
this function for google api key acces in html template 
'''

def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}