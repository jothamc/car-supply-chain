from django.db import models
# from manufacturers.models import Manufacturer

# Create your models here.

class Car(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.CASCADE, null=True )
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blueprints:detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return "%s %s" % (self.manufacturer,self.name)