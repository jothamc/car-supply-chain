# Generated by Django 3.0.5 on 2020-05-02 03:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealerships', '0003_auto_20200502_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealership',
            name='balance',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]