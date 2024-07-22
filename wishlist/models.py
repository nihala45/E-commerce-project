from django.db import models

# Create your models here.

class  WishlistProduct(models.Model):
    user = models.ForeignKey('logintohome.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey('products.newproducts', on_delete=models.CASCADE)
    