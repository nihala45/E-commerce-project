# Generated by Django 5.0.6 on 2024-08-02 15:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('couponmanagement', '0008_remove_coupon_discount_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponusage',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='couponmanagement.coupon'),
        ),
    ]
