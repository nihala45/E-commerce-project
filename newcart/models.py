# Create your models here.
from django.db import models
from logintohome.models import CustomUser
from products.models import newproducts
from userprofile.models import UserAddress
from couponmanagement.models import Coupon


class  MyCart(models.Model):
    SIZE_CHOICES = [
        ('s', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large'),
    ]
    user = models.ForeignKey('logintohome.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey('products.newproducts', on_delete=models.CASCADE)
   
    discount_percentage = models.PositiveIntegerField(default=0)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    
    
    @property
    def total_amount(self):
        return self.quantity * self.product.price
    
    @property
    def get_discount_cart_total(self):
        if self.product.offer and self.product.offer.discount:
            return (self.product.price - self.product.offer.discount)*(self.quantity)
        return self.total_amount
    
    

    

class AllOrder(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    order_date=models.DateField()
    payment_method=models.CharField(max_length=100)
    total_amount=models.IntegerField()
    discount_amount=models.IntegerField()
    

class Ordered_item(models.Model):
    order=models.ForeignKey(AllOrder,on_delete=models.CASCADE)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default="Pending")
    product = models.ForeignKey(newproducts, on_delete=models.CASCADE)
    product_qty = models.PositiveIntegerField()
    product_size=models.CharField(max_length=10)
    
    
