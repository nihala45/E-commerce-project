# Generated by Django 5.0.6 on 2024-07-04 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('logintohome', '0001_initial'),
        ('products', '0005_delete_varients'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('prod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.newproducts')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logintohome.customuser')),
            ],
        ),
    ]
