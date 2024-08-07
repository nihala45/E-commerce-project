from django.db import models
from category.models import categories
from offermanagement.models import Offer
# Create your models here.

class newproducts(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(categories, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image1 = models.ImageField(upload_to='images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='images/', blank=True, null=True)
    small = models.CharField(max_length=50)
    medium = models.CharField(max_length=50)
    large = models.CharField(max_length=50)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, blank=True, null=True)
    
    def get_discounted_price(self):
        if self.offer and self.offer.discount:
            return self.price - self.offer.discount
        return self.price 
   


   
# class varients(models.Model):
#     product_id = models.ForeignKey(newproducts,on_delete=models.CASCADE)
#     small = models.CharField(max_length=50)
#     medium = models.CharField(max_length=50)
#     large = models.CharField(max_length=50)
    
    
 