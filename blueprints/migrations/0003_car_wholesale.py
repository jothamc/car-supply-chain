# Generated by Django 3.0.5 on 2020-04-29 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blueprints', '0002_car_manufacturer'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='wholesale',
            field=models.BooleanField(default=False),
        ),
    ]
