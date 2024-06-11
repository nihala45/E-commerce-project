# Generated by Django 5.0.6 on 2024-06-08 06:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_products_image1_products_image2_products_image3_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='newproducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image1', models.ImageField(blank=True, null=True, upload_to='static/images/products/')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='static/images/products/')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='static/images/products/')),
                ('image4', models.ImageField(blank=True, null=True, upload_to='static/images/products/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.categories')),
            ],
        ),
        migrations.DeleteModel(
            name='products',
        ),
    ]
