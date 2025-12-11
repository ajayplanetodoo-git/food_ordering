from django import forms
from .models import User ,UserProfile
from django.contrib.auth import get_user_model

class Userform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields =["first_name","last_name","username","email","phone_number","password","confirm_password"]

    def clean(self):
        cleaned_data = super(Userform,self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password!=confirm_password:
            raise forms.ValidationError("Password is not match")
        

    # def clean_username(self): # in this function we are validating suername if it already exixt using get_user_model
    #     User = get_user_model()
    #     username = self.cleaned_data.get("username")
    #     qs = User.objects.filter(username=username) # here filter data
    #     if qs.exists():
    #         raise forms.ValidationError("Username is already taken")
    #     return username

    # def clean_email(self):
    #      User = get_user_model()
    #      email = self.cleaned_data.get("email")
    #      qs = User.objects.filter(email=email)
    #      if qs.exists():
    #          raise forms.ValidationError("Email email is already exist")
    #      return email

    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"
        exclude = ("user",)