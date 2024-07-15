from django.db import models
from logintohome.models import CustomUser

# Create your models here.



class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address_name = models.CharField(max_length=100)
    address_Email = models.EmailField()
    address_Phone = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    landmark =models.CharField(max_length=100)
    city =models.CharField(max_length=100)
    district =models.CharField(max_length=100)
    state =models.CharField(max_length=100)
    pin =models.CharField(max_length=100)
    