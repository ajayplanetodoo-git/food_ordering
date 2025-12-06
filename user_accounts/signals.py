from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User ,UserProfile






'''
here we are create reciever function which automaticaly creates userprofile at the time of user created 
it requred sender which is our User (usermodel) and receiver
there are two type of specify reciver using decoraters 
1st :@receiver(post_save,sender=User) 
post_save.connect(post_save_signal_create_profile_receiver,sender=User)
'''
@receiver(post_save,sender=User)
def post_save_signal_create_profile_receiver(sender,instance,created,**kwargs):
    print(created)
    if created: # for creation of userprofile
        UserProfile.objects.create(user=instance)
        print("User Profile is created")
    else:
        try:  # for updation in userprofile 
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            # create user profile if not exist
            UserProfile.objects.create(user=instance)
            print("user profile is not exist but ,i created one")

@receiver(pre_save,sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username,"This User being save")