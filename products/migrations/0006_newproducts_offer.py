# Generated by Django 5.0.6 on 2024-07-27 15:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offermanagement', '0001_initial'),
        ('products', '0005_delete_varients'),
    ]

    operations = [
        migrations.AddField(
            model_name='newproducts',
            name='offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='offermanagement.offer'),
        ),
    ]
