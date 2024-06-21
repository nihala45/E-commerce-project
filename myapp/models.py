from django.db import models
from django.shortcuts import redirect
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
import pyotp
from django.contrib.auth.views import LoginView
from category.models import categories

# Create your models here.
# class CustomUser(models.Model):
#     username=models.CharField(max_length=50)
#     email=models.EmailField(unique=True)
#     password=models.CharField(max_length=50)
#     phone = models.CharField(max_length=100)
#     otp_secret = models.CharField(max_length=200)
#     otp_fld = models.CharField(max_length=70)
#     is_blocked = models.BooleanField(default=False)

# def generate_otp(user):
#     secret_key = pyotp.random_base32()
#     otp = pyotp.TOTP(secret_key)
#     otp_code = otp.now()
#     print('hello',otp_code)
#     user.otp_secret = secret_key
#     user.otp_fld = otp_code
#     user.save()    
#     return otp_code


# def send_otp_email(instance,otp_code):
#     subject="OTP Varification"
#     message=f"Your OTP for verification is:{otp_code}"
#     from_email="nihalashirin02@gmail.com"
#     send_mail(subject,message,from_email,[instance.email])
    

# @receiver(post_save,sender=CustomUser)
# def generate_and_send_otp(sender,instance,created,**kwargs):
#     if created:
#         otp_code = generate_otp(instance)
#         send_otp_email(instance,otp_code)
        

    

# class newproducts(models.Model):
#     name = models.CharField(max_length=255)
#     category = models.ForeignKey(categories, on_delete=models.CASCADE)
#     description = models.TextField(blank=True, null=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
    
#     image1 = models.ImageField(upload_to='static/images/products/', blank=True, null=True)
#     image2 = models.ImageField(upload_to='static/images/products/', blank=True, null=True)
#     image3 = models.ImageField(upload_to='static/images/products/', blank=True, null=True)
#     image4 = models.ImageField(upload_to='static/images/products/', blank=True, null=True)
#     # small = models.CharField(max_length=50)
#     # medium = models.CharField(max_length=50)
#     # large = models.CharField(max_length=50)

# class UserAddress(models.Model):
#     # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     address_name = models.CharField(max_length=100)
#     address_Email = models.EmailField(unique=True)
#     address_Phone = models.CharField(max_length=100)
#     Address = models.CharField(max_length=100)
#     landmark =models.CharField(max_length=100)
#     city =models.CharField(max_length=100)
#     district =models.CharField(max_length=100)
#     state =models.CharField(max_length=100)
#     pin =models.CharField(max_length=100)
    
    
    
    
# class varients(models.Model):
#     product_id = models.ForeignKey(newproducts,on_delete=models.CASCADE)
#     small = models.CharField(max_length=50)
#     medium = models.CharField(max_length=50)
#     large = models.CharField(max_length=50)
    
    
 
 
    