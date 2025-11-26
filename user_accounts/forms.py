from django import forms
from .models import User


class userform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields =["first_name","last_name","username","email","phone_number","password","confirm_password"]

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("Password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Password is not match")
        return data
    
    def full_clean(self):
        return super().full_clean()