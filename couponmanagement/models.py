from django.db import models
from django.utils import timezone

class Coupon(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True) 
    percentage = models.PositiveIntegerField()  # Changed to PositiveIntegerField for non-negative values
    date = models.DateField()
    expiry_date = models.DateField()

    def is_active(self):
        today = timezone.now().date()
        return self.date <= today <= self.expiry_date

    def __str__(self):
        return f"{self.name} - {self.percentage}%"