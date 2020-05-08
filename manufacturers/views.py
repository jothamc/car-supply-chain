from django import forms
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView

from blueprints.models import Car
from inventory.models import WholesaleCar
from users.permissions import UserIsManufacturer

from .models import Manufacturer, ManufacturingOrder

# Create your views here.


class ManufacturingOrderForm(forms.ModelForm):
    """ Form definition for manufacturing order
    
    Creates a form for manufacturing order showing only blueprints
    created by the manufacturer.

    Parameters:
        user (obj): The current user object (request.user)

    Returns a manufacturung order model form.
    """

    class Meta:
        model = ManufacturingOrder
        fields = ("car","count")

    def __init__(self, user, *args, **kwargs):
        """
        The constructor for ManufacturingOrder form
        
        Parameters:
            user (obj): the current user object (request.user)
        """

        super().__init__(*args, **kwargs)
        self.fields['car'].queryset = Car.objects.filter(
            manufacturer__admin=user)


@method_decorator(transaction.atomic, name="form_valid")
class ManufacturingOrderCreateView(UserIsManufacturer, CreateView):
    """
    CreateView for Manufacturing Orders.

    A view for creating manufacturing orders. Passes the current user object to 
    the model form to obtain a personalied form.
    When the form is returned, the total cost of the manufacturing order is
    deducted from the manufacturer's balance and new Wholesale cars
    corresponding to the specifications in the manufacturing order are
    created.

    Diplays an error when the  manufacturer's balance is lesser than the
    total cost.
    Redirects to the manufacturing order detail view if successful.
    """

    model = ManufacturingOrder
    template_name = "manufacturing-order-create.html"

    def get_form(self):
        return ManufacturingOrderForm(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        car = form.instance.car
        count = form.instance.count

        total_cost = car.price * count
        balance = car.manufacturer.balance

        if balance >= total_cost:
            form.instance.manufacturer = car.manufacturer
            manufacturing_order = form.save()

            car.manufacturer.balance = F('balance') - total_cost
            car.manufacturer.save()

            wholesale, _ = WholesaleCar.objects.update_or_create(
                name=car.name,
                cost_price=car.price,
                selling_price=car.price,
                manufacturer=car.manufacturer)
            wholesale.amount = F('amount') + count
            wholesale.save()

            success_url = "manufacturers:mo_detail"
            return redirect(success_url, manufacturing_order.pk)
        else:
            form.add_error(field=None, error="Your balance is too low")
            return self.form_invalid(form)


class ManufacturingOrderDetailView(UserIsManufacturer, DetailView):
    """ Detail View to show Manufacturing Orders"""

    model = ManufacturingOrder
    template_name = "manufacturing-order-detail.html"
    context_object_name = "manu_order"

    def get_object(self):
    # Prevent non owners (manufacturers) from access
        obj = super().get_object()
        if obj.manufacturer != self.request.user.manufacturer_set.get():
            raise PermissionDenied
