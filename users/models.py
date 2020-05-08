from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class User(AbstractUser):
    """Model definition for User."""

    CUSTOMER = "CU"
    DEALERSHIP = "DE"
    MANUFACTURER = "MA"
    USER_TYPE = (
        (CUSTOMER, "Customer"),
        (DEALERSHIP, "Dealership Admin"),
        (MANUFACTURER, "Manufacturer Admin"),
    )

    balance = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(1)])
    user_type = models.CharField(
        max_length=2, choices=USER_TYPE, default=CUSTOMER)
