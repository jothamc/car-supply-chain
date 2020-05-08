# Generated by Django 3.0.5 on 2020-04-29 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wholesalecar',
            name='selling_price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='wholesalecar',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
    ]