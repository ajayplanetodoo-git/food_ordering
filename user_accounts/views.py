from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import userform
from .models import User

# Create your views here.
def registeruser(request):
    if request.method=="POST":
        print(request.POST)
        form = userform(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # here are form are ready to save grab all data 
            user.role = User.CUSTOMER # here is we are assinged user role
            user.save()
            return redirect("userregister")
    else:
        form = userform()
    context = {
        "forms" : form,
    }
    return render(request,"user_accounts/registration.html",context)

