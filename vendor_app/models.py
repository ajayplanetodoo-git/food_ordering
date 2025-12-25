from django.db import models
from user_accounts.models import User ,UserProfile 
from user_accounts.utils import send_notification

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

