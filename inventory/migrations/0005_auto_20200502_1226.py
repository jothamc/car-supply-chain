# Generated by Django 3.0.5 on 2020-05-02 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturers', '0008_auto_20200502_0423'),
        ('inventory', '0004_auto_20200501_0441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='retailcar',
            name='car',
        ),
        migrations.RemoveField(
            model_name='wholesalecar',
            name='car',
        ),
        migrations.AddField(
            model_name='retailcar',
            name='cost_price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='retailcar',
            name='manufacturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='manufacturers.Manufacturer'),
        ),
        migrations.AddField(
            model_name='retailcar',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='wholesalecar',
            name='cost_price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='wholesalecar',
            name='manufacturer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manufacturers.Manufacturer'),
        ),
        migrations.AddField(
            model_name='wholesalecar',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
