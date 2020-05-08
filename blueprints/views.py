from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from guardian.shortcuts import assign_perm
from guardian.mixins import PermissionRequiredMixin

from manufacturers.views import UserIsManufacturer

from .models import Car

# Create your views here.


class BlueprintCreateView(UserIsManufacturer,CreateView):
    """ Create view for Blueprint. """

    model = Car
    template_name = "blueprint-create.html"
    fields = ("name", "price")

    def form_valid(self, form):
        form.instance.manufacturer = self.request.user.manufacturer_set.get()
        car = form.save()
        assign_perm("view_car", self.request.user, car)
        assign_perm("change_car", self.request.user, car)
        return super().form_valid(form)


class BlueprintDetailView(PermissionRequiredMixin, DetailView):
    """ Detail view for Blueprint. """

    model = Car
    template_name = "blueprint-detail.html"
    context_object_name = "blueprint"
    permission_required = "change_car"
    raise_exception = True

class BlueprintUpdateView(PermissionRequiredMixin, UpdateView):
    """ Update view for Blueprint. """

    model = Car
    template_name = "blueprint-edit.html"
    fields = ("name", "price")
    context_object_name = "blueprint"

    permission_required = "change_car"
    raise_exception = True



class BlueprintListView(UserIsManufacturer, ListView):
    """ List view for Blueprint. """

    template_name = "blueprint-list.html"
    context_object_name = "blueprints"

    def get_queryset(self):
        return Car.objects.filter(manufacturer__admin=self.request.user)


class BluePrintDeleteView(PermissionRequiredMixin, DeleteView):
    """ Delete view for Blueprint. """

    model = Car
    template_name = "blueprint-delete.html"
    context_object_name = "blueprint"
    success_url = reverse_lazy("blueprints:index")

    permission_required = "change_car"
    raise_exception = True