from django.db import models

from blueprints.models import Car
from dealerships.models import Dealership
from manufacturers.models import Manufacturer

# Create your models here.



class WholesaleCar(models.Model):
    """ Model definition for wholesale car.""" 
    
    name = models.CharField(max_length=50, null=True)
    cost_price = models.PositiveIntegerField(default=0)
    wholesale_price = models.PositiveIntegerField(default=0)
    amount = models.PositiveIntegerField(default=0)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE,null=True)


    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('inventory:wholesale_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "%s %s" % (self.manufacturer,self.name)


class RetailCar(models.Model):
    """ Model definition for retail car. """

    name = models.CharField(max_length=50, null=True)
    cost_price = models.PositiveIntegerField(default=0)
    retail_price = models.PositiveIntegerField(default=0)
    amount = models.PositiveIntegerField(default=0)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE,null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.DO_NOTHING, null=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('inventory:retail_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "%s %s" % (self.manufacturer,self.name)
