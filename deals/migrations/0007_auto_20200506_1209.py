# Generated by Django 3.0.5 on 2020-05-06 11:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0006_wholesaledeal_asking_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wholesaledeal',
            name='amount',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]