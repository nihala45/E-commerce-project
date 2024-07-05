from django.db import models
from logintohome.models import CustomUser
from products.models import newproducts

# # Create your models here.
class  MyCart(models.Model):
    SIZE_CHOICES = [
        ('s', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large'),
    ]
    user = models.ForeignKey('logintohome.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey('products.newproducts', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES)
    
    @property
    def total_amount(self):
        return self.quantity * self.product.price