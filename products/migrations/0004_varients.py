# Generated by Django 5.0.6 on 2024-07-04 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_newproducts_image1_alter_newproducts_image2_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='varients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small', models.CharField(max_length=50)),
                ('medium', models.CharField(max_length=50)),
                ('large', models.CharField(max_length=50)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.newproducts')),
            ],
        ),
    ]