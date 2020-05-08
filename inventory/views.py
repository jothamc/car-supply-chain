from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from users.permissions import (UserIsCustomer, UserIsDealership,
                               UserIsManufacturer, UserIsNotCustomer)

from .models import RetailCar, WholesaleCar

# Create your views here.


class WholesaleCarDetailView(UserIsManufacturer, DetailView):
    """ Detail view for Wholesale cars"""

    model = WholesaleCar
    template_name = "inventory/manufacturers/wholesale_car_detail.html"
    context_object_name = "car"

    def get_object(self):
        # object-level Permission
        obj = super().get_object()
        if self.request.user != obj.manufacturer.admin:
            raise PermissionDenied
        return obj


class CarListView(UserIsNotCustomer, ListView):
    """ List view for cars in inventory 

    If user is manufacturer admin, shows all wholesale cars in manufacturer's inventory
    If user is dealership admin, shows all wholesale cars in dealership's inventory
    """

    template_name = "inventory_list.html"
    context_object_name = "cars"

    def get_queryset(self):
        from users.models import User
        user_type = self.request.user.user_type

        if user_type == User.MANUFACTURER:
            self.template_name = "inventory/manufacturers/inventory_list.html"
            return WholesaleCar.objects.filter(manufacturer__admin=self.request.user, amount__gt=0)
        elif user_type == User.DEALERSHIP:
            self.template_name = "inventory/dealerships/inventory_list.html"
            return RetailCar.objects.filter(dealership__admin=self.request.user, amount__gt=0)


class WholesaleCarUpdateView(UserIsManufacturer, UpdateView):
    """ Update view for wholesale car. """

    model = WholesaleCar
    template_name = "inventory/manufacturers/wholesale_car_update.html"
    context_object_name = "car"
    fields = ("selling_price",)

    def get_object(self):
        obj = super().get_object()
        if self.request.user != obj.manufacturer.admin:
            raise PermissionDenied
        return obj


class WholesaleCarDeleteView(UserIsManufacturer, DeleteView):
    """ Delete view for wholesale car. """

    model = WholesaleCar
    template_name = "inventory/manufacturers/wholesale_car_delete.html"
    context_object_name = "car"
    success_url = reverse_lazy("inventory:index")

    def get_object(self):
        obj = super().get_object()
        if self.request.user != obj.manufacturer.admin:
            raise PermissionDenied
        return obj


class AllWholesaleCarListView(UserIsDealership, ListView):
    """ List view to list all cars by all manufacturers """

    template_name = "inventory/dealerships/wholesale_car_list.html"
    context_object_name = "cars"

    def get_queryset(self):
        return WholesaleCar.objects.filter(amount__gt=0)


class AllRetailCarListView(UserIsCustomer, ListView):
    """ List view showing all cars owned by all dealerships. """

    template_name = "inventory/customers/retail_car_list.html"
    context_object_name = "cars"

    def get_queryset(self):
        return RetailCar.objects.filter(amount__gt=0)


class RetailCarDetailView(UserIsDealership, DetailView):
    """ Detail view for retail cars. """

    model = RetailCar
    template_name = "inventory/dealerships/retail_car_detail.html"
    context_object_name = "car"

    def get_object(self):
        obj = super().get_object()
        if self.request.user != obj.dealership.admin:
            raise PermissionDenied
        return obj


class RetailCarUpdateView(UserIsDealership, UpdateView):
    """ Update view for retail cars. """

    model = RetailCar
    template_name = "inventory/dealerships/retail_car_update.html"
    context_object_name = "car"
    fields = ("selling_price",)

    def get_object(self):
        obj = super().get_object()
        if self.request.user != obj.dealership.admin:
            raise PermissionDenied
        return obj


class RetailCarDeleteView(UserIsDealership, DeleteView):
    """ Delete view for retail cars. """
    
    model = RetailCar
    template_name = "inventory/dealerships/retail_car_delete.html"
    context_object_name = "car"
    success_url = reverse_lazy("inventory:index")

    def get_object(self):
        obj = super().get_object()
        if self.request.user != obj.dealership.admin:
            raise PermissionDenied
        return obj
