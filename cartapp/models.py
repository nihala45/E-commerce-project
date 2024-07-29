from django.db import models
from logintohome.models import CustomUser
from products.models import newproducts
from userprofile.models import UserAddress


# # Create your models here.
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
    
    @property
    def total_amount(self):
        return self.quantity * self.product.price
    
    @property
    def get_discount_cart_total(self):
        if self.product.offer and self.product.offer.discount:
            return (self.product.price - self.product.offer.discount)*(self.quantity)
        return self.total_amount
    
    
class Orders(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ordered_date = models.DateField()
    # delivered_date = models.DateField(null=True)
    payment_method = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="Pending")
    # return_status = models.CharField(max_length=100, null=True, blank=True)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
    product = models.ForeignKey(newproducts, on_delete=models.CASCADE)
    discount_amt = models.DecimalField(max_digits=30, decimal_places=1, default=0)
    product_qty = models.PositiveIntegerField()  
    product_price=models.IntegerField()
    product_size=models.CharField(max_length=10)
                                