from django.db import models
from django.utils import timezone
from logintohome.models import CustomUser
class Coupon(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True) 
    percentage = models.PositiveIntegerField()  
    name = models.CharField(max_length=100)
    critiria_amount = models.IntegerField()
    date = models.DateField()
    expiry_date = models.DateField() 

    def is_active(self):
        today = timezone.now().date()
        return self.date <= today <= self.expiry_date

    def __str__(self):
        return f"{self.name} - {self.percentage}%"
    

class CouponUsage(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)