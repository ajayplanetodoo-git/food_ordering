
from vendor_app.models import Vendor , UserProfile
from django.conf import settings

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor=None
    return dict(vendor=vendor)

def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)   
    except:
        user_profile = None
    return dict(user_profile=user_profile)

'''
this function for google api key acces in html template 
'''

def get_google_api(request):
    return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}