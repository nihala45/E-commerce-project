from django.db import models

# Create your models here.


class categories(models.Model):
    category_name=models.CharField(max_length=50)