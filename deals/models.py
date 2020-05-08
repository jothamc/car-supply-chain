from django.db import models
from django.core.validators import MinValueValidator

from inventory.models import WholesaleCar, RetailCar
from dealerships.models import Dealership
from users.models import User


# Create your models here.

class WholesaleDeal(models.Model):
    """ Model definition for Wholesale deal. """

    ACCEPTED = "AC"
    PENDING = "PE"
    REJECTED = "RE"
    STATUS = (
        (PENDING,"PENDING"),
        (ACCEPTED,"ACCEPTED"),
        (REJECTED,"REJECTED"),
    )
    
    status = models.CharField(max_length=2,choices=STATUS, default=PENDING)
    car = models.ForeignKey(WholesaleCar, on_delete=models.CASCADE)
    asking_price = models.PositiveIntegerField(default=0)
    amount = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("deals:wholesale_deal_detail", kwargs={"pk":self.pk})


class RetailDeal(models.Model):
    """ Model definition for Retail deal. """

    ACCEPTED = "AC"
    PENDING = "PE"
    REJECTED = "RE"
    STATUS = (
        (PENDING,"PENDING"),
        (ACCEPTED,"ACCEPTED"),
        (REJECTED,"REJECTED"),
    )
    
    status = models.CharField(max_length=2,choices=STATUS, default=PENDING)
    car = models.ForeignKey(RetailCar, on_delete=models.CASCADE)
    asking_price = models.PositiveIntegerField(default=0)
    amount = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("deals:retail_deal_detail", kwargs={"pk":self.pk})
