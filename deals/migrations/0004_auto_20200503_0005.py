# Generated by Django 3.0.5 on 2020-05-02 23:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20200502_1226'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dealerships', '0004_auto_20200502_0418'),
        ('deals', '0003_auto_20200501_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wholesaledeal',
            name='amount',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='wholesaledeal',
            name='dealership',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dealerships.Dealership'),
        ),
        migrations.CreateModel(
            name='RetailDeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PE', 'PENDING'), ('AC', 'ACCEPTED'), ('RE', 'REJECTED')], default='PE', max_length=2)),
                ('amount', models.PositiveIntegerField(default=1)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.RetailCar')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
