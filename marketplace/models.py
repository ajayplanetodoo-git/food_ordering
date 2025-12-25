from django.db import models
from user_accounts.models import User
from menu.models import FoodIteam

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditeam = models.ForeignKey(FoodIteam,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user