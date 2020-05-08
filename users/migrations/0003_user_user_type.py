# Generated by Django 3.0.5 on 2020-04-29 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('CU', 'Customer'), ('DE', 'Dealership'), ('MA', 'Manufacturer')], default='CU', max_length=2),
        ),
    ]
