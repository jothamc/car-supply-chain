from django.contrib import admin
from .models import Manufacturer, ManufacturingOrder
# Register your models here.
admin.site.register(Manufacturer)
admin.site.register(ManufacturingOrder)