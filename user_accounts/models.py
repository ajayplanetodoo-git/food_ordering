from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager

from django.contrib.auth import get_user_model

# Create your models here.
'''usermanager cannot create or hold any fields it only contain methods 
BaseUsermanager check how and what used sholud be created like normaluser or Superuser
when normal user it call create_user function
'''
class UserManeger(BaseUserManager):
    '''
    when if you want to create user or superuser from anywhere this two function create_user and createsuperuser  are required always 
    without this two function cannot create any user and hasing things

    '''
    
    def create_user(self,first_name, last_name,username, email, password=None):
        if not email:
            raise ValueError("User must have email address")
        if not username :
            raise ValueError("User must have username ")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,

        )
        user.set_password(password) 
        user.save(using =self._db)
        return user
    
    #  when user is super user then this call create_superuser  function it basicall for admin pandel login  python manage.py cretaesuperuser
    #  insted of defult username it will ask for email  urls : 8000/admin
    def create_superuser(self,first_name, last_name,username, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password= password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin =True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    RESTAURANT = 1
    CUSTOMER = 2
    ROLE_CHOICE = (
        (RESTAURANT ,"Restaurant"),
        (CUSTOMER , "Customer"),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100 , unique=True)
    phone_number =  models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)

    # required fileds
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name',"last_name"]

    objects = UserManeger()
    def __str__(self):
        return self.email

    def has_perm(self,perms, obj=None):
        return self.is_admin

    def has_module_perms(self,app_lable):
        return True
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True,null=True)
    profile_picture = models.ImageField(upload_to='core/media/user',blank=True,null=True)
    cover_picture = models.ImageField(upload_to='core/media/user',blank=True,null=True)
    address_line_1 = models.CharField(max_length=50,blank=True,null=True)
    address_line_2 = models.CharField(max_length=50,blank=True,null=True)
    country = models.CharField(max_length=15,blank=True,null=True)
    state = models.CharField(max_length=15,blank=True,null=True)
    city = models.CharField(max_length=15,blank=True,null=True)
    pincode = models.CharField(max_length=6,blank=True,null=True)
    latitude = models.CharField(max_length=20,blank=True,null=True)
    longitude = models.CharField(max_length=20,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email








