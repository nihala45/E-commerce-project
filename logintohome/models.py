from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
import pyotp

# Create your models here.
class CustomUser(models.Model):
    username=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=50)
    phone = models.CharField(max_length=100)
    otp_secret = models.CharField(max_length=200)
    otp_fld = models.CharField(max_length=70)
    is_blocked = models.BooleanField(default=False)

def generate_otp(user):
    secret_key = pyotp.random_base32()
    otp = pyotp.TOTP(secret_key)
    otp_code = otp.now()
    print('hello',otp_code)
    user.otp_secret = secret_key
    user.otp_fld = otp_code
    user.save()    
    return otp_code


def send_otp_email(instance,otp_code):
    subject="OTP Varification"
    message=f"Your OTP for verification is:{otp_code}"
    from_email="nihalashirin02@gmail.com"
    send_mail(subject,message,from_email,[instance.email])
    

@receiver(post_save,sender=CustomUser)
def generate_and_send_otp(sender,instance,created,**kwargs):
    if created:
        otp_code = generate_otp(instance)
        send_otp_email(instance,otp_code)