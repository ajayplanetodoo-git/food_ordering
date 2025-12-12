from django import forms
from user_accounts.models import User
from .models import Vendor
from user_accounts.validator import img_field_validation


class Vendorform (forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class':'btn-btn-info'}),validators=[img_field_validation])

    class Meta:
        model = Vendor
        fields = ['vendor_name','vendor_license']
