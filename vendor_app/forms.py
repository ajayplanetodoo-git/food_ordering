from django import forms
from user_accounts.models import User
from .models import Vendor

class Vendorform (forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['vendor_name','vendor_license']
