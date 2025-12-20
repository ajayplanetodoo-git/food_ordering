from django import forms
from user_accounts.validator import img_field_validation
from .models import Category , FoodIteam

class Category_form(forms.ModelForm):
    class Meta:
        model = Category
        fields =["category_name",'description']

class FoodIteam_form(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class':'btn-btn-info w-100'}),validators=[img_field_validation])
    class Meta:
        model = FoodIteam
        fields =['category','food_title','description','price','image','is_available']
        