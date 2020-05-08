import json

from django.core.validators import MinValueValidator
from django.db import models

from blueprints.models import Car
from users.models import User

with open("countries-django.json") as file:
    countries = json.loads(file.read())


# Create your models here.
class Manufacturer(models.Model):
    """Model definition for Manufacturer. """

    name = models.CharField(max_length=30)
    country = models.CharField(max_length=3, choices=countries)
    balance = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(1)])
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class ManufacturingOrder(models.Model):
    """Model definition for Manufacturing Order """
    
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, null=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    count = models.PositiveIntegerField()

    def __str__(self):
        return "%d - %d %ss" % (self.pk, self.count, self.car)
