# Generated by Django 5.0.6 on 2024-08-02 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newcart', '0005_alter_mycart_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='allorder',
            name='discount_amount',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]