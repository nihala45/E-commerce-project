# Generated by Django 5.0.6 on 2024-07-19 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('discount', models.IntegerField()),
                ('active_date', models.DateField()),
                ('expiry_date', models.DateField()),
            ],
        ),
    ]
