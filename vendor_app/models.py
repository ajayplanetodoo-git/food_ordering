from django.db import models
from user_accounts.models import User ,UserProfile 
from user_accounts.utils import send_notification
from datetime import date , datetime , time

from django.utils import timezone
import pytz
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name="vendor",on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name="vendor",on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to="vendor_app/license")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.vendor_name
    
#  function in side model class is called member Function this function act as vendors field vendor.is_open
# Check current day's opening Hours. 
    def is_open(self):
        today_date = date.today()
        day= today_date.isoweekday()

        current_opening_hours = OpeningHour.objects.filter(vendor=self,day=day)
        now = timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))
        current_time = now.strftime("%H:%M:%S")
        print(current_time)

        is_open =None
        for i in current_opening_hours:
            if not i.is_closed:
                start = str(datetime.strptime(i.from_hour,'%I:%M %p').time())
                end = str(datetime.strptime(i.to_hour,'%I:%M %p').time())
                if current_time > start and current_time<end:
                    is_open = True
                    break
                else:
                    is_open = False        
        return is_open                                                                                         

# This is for overide defult  save function in admin planel for vendar is approved  
# button checked if and i will send emai;l using help guction
    def save(self,*args,**kwargs):
        if self.pk is not None:
            #update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'user_accounts/emails/admin_approval_email.html'
                context =  {
                    'user' : self.user,
                    'is_approved' : self.is_approved,
                    'to_email' : self.user.email,
                }
                if self.is_approved == True:
                    #send notification email
                    mail_subject = "congratualtion your restront is approved"
                    send_notification(mail_subject,mail_template,context)
                else:
                    # send notification email
                    mail_subject = "we're  sorry you are nor eligible for publishing your menu on your marketplace "
                    send_notification(mail_subject,mail_template,context)
        return super(Vendor,self).save(*args, **kwargs)


DAYS=[
    (1,('Monday')),
    (2,('Tuesday')),
    (3,('Wednesday')),
    (4,('Thurstday')),
    (5,('Friday')),
    (6,('Saturday')),
    (7,('Sunday')),

]

HOUR_OF_DAY_DAY = t = [(time(h,m).strftime('%I:%M %p'),time(h,m).strftime('%I:%M %p')) for h in range(0,24) for m in (0,30)]

class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.Case)
    day=models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_DAY,max_length=10 ,blank=True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_DAY,max_length=10,blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering =('day','-from_hour')
        unique_together = ('vendor','day','from_hour','to_hour')

    def __str__(self):
        return self.get_day_display() # get_fieldname_display tgis in built function show me choice field 
                                    # ex: (1,'Monday)  so it modnay show in html insted of 1
