from django.db import models
from django.core.validators import MinValueValidator


import json
with open("countries-django.json") as file:
    countries = json.loads(file.read())
from users.models import User

# Create your models here.
class Dealership(models.Model):
    """Model definition for Dealership. """

    name = models.CharField(max_length=30)
    country = models.CharField(max_length=3,choices=countries)
    balance = models.PositiveIntegerField(default=0,validators=[MinValueValidator(1)])
    admin = models.ForeignKey(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name