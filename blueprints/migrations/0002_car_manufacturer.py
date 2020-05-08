# Generated by Django 3.0.5 on 2020-04-28 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturers', '0002_manufacturingorder'),
        ('blueprints', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='manufacturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='manufacturers.Manufacturer'),
        ),
    ]