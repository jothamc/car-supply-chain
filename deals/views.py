from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import F
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, ListView

from inventory.models import RetailCar, WholesaleCar
from users.permissions import (UserIsCustomer, UserIsDealership,
							   UserIsManufacturer, UserIsNotCustomer,
							   UserIsNotManufacturer)

from .models import RetailDeal, WholesaleDeal

# Create your views here.
from guardian.shortcuts import assign_perm
from guardian.mixins import PermissionRequiredMixin

class WholesaleDealForm(forms.ModelForm):
	"""Form definition for WholesaleDeal.

	Form for wholesale deal creation. Requires the primary
	key of the car involved in the wholesale deal to set the queryset.

	Parameters:
		car_pk (int): The primary key of the car involved in the deal


	"""

	class Meta:
		model = WholesaleDeal
		fields = ("car", "amount", "asking_price")

	def __init__(self, car_pk, *args, **kwargs):
		"""
		Constructor for Wholesale deal form.

		Sets the car field queryset to show only the car involved in the deal
		Sets the initial asking price to the car selling price (to encourage higher prices).
		Sets the amount field widget attributes:
			maximum value: to total number of wholesale cars in stock
			minimum: to 1

		"""

		super().__init__(*args, **kwargs)
		car_queryset = WholesaleCar.objects.filter(pk=car_pk)
		self.initial['car'] = car_queryset[0]
		self.initial['asking_price'] = car_queryset[0].wholesale_price
		self.fields['car'].queryset = car_queryset
		self.fields['amount'].widget.attrs.update({
			"max": car_queryset[0].amount,
			"min": 1
		})


class WholesaleDealCreateView(UserIsDealership, CreateView):
	"""
	Create View to initialize a wholesale deal.


	"""

	template_name = "wholesale_deal_create.html"
	form_class = WholesaleDealForm

	def get_form(self):
		""" Instantiates the wholesale deal form and return it. """

		car_pk = self.kwargs.get("pk")
		return WholesaleDealForm(car_pk, **self.get_form_kwargs())

	def form_valid(self, form):
		""" Creates the deals or displays an error if dealership balance is low. """

		total_cost = form.instance.asking_price
		form.instance.dealership = self.request.user.dealership_set.get()

		if form.instance.dealership.balance < total_cost:
			form.add_error(field=None, error="Your balance is too low")
			return self.form_invalid(form)

		deal = form.save()

		manufacturer_admin = form.instance.car.manufacturer.admin
		assign_perm("view_wholesaledeal", self.request.user, deal)
		assign_perm("view_wholesaledeal", manufacturer_admin, deal)
		assign_perm("change_wholesaledeal", manufacturer_admin, deal)

		return super().form_valid(form)


class WholesaleDealDetailView(PermissionRequiredMixin, DetailView):
	""" Detail view for wholesale deals. """

	model = WholesaleDeal
	template_name = "wholesale_deal_detail.html"
	context_object_name = "deal"

	permission_required = "view_wholesaledeal"
	raise_exception = True


class WholesaleDealListView(UserIsManufacturer, ListView):
	""" List view showing all deals made to a manufacturer by dealership admins."""

	template_name = "wholesale_deal_list.html"
	context_object_name = "deals"

	def get_queryset(self):
		return WholesaleDeal.objects.filter(car__manufacturer__admin=self.request.user)


class RetailDealListView(UserIsDealership, ListView):
	""" List view showing all deals made to a dealership by customers. """

	template_name = "retail_deal_list.html"
	context_object_name = "deals"

	def get_queryset(self):
		return RetailDeal.objects.filter(car__dealership__admin=self.request.user)


@login_required
@transaction.atomic
def acceptWholesaleDeal(request, pk):
	""" View to accept a wholesale deal

	This view deducts the total price of the deal from the dealership
	balance and adds it to the manufacturer's balance.
	It also deducts the amount of wholesale cars specified in the deal
	from the manufacturer's inventory and adds it to the dealership's
	inventory as retail cars.
	The deal status is updated to accepted

	Parameters:
		request (WSGI request): current request instance
		pk (int): primary key of wholesale deal

	Redirects to the wholesale deal detail view
	"""

	deal = WholesaleDeal.objects.get(pk=pk)
	manufacturer = deal.car.manufacturer

	if not manufacturer.admin.has_perm("change_wholesaledeal", deal):	
		raise PermissionDenied

	total_cost = deal.asking_price
	dealership_balance = deal.dealership.balance
	if deal.status == WholesaleDeal.PENDING and dealership_balance >= total_cost:

		deal.dealership.balance = F('balance') - total_cost
		deal.dealership.save()

		manufacturer.balance = F('balance') + total_cost
		manufacturer.save()

		retail, _ = RetailCar.objects.update_or_create(
			name=deal.car.name,
			cost_price=deal.car.wholesale_price,
			retail_price=deal.car.wholesale_price,
			manufacturer=deal.car.manufacturer,
			dealership=deal.dealership
		)
		retail.amount = F('amount') + deal.amount
		retail.save()

		deal.car.amount = F('amount') - deal.amount
		deal.car.save()

		deal.status = WholesaleDeal.ACCEPTED
		deal.save()

		return redirect("deals:wholesale_deal_detail", pk)
	else:
		return redirect("deals:wholesale_deal_detail", pk)


@login_required
def rejectWholesaleDeal(request, pk):
	""" View to reject a wholesale deal.

	This view sets the deal status to REJECTED.
	Redirects to the wholesale deal detail view.
	"""

	deal = WholesaleDeal.objects.get(pk=pk)
	manufacturer = deal.car.manufacturer

	if not manufacturer.admin.has_perm("change_wholesaledeal", deal):	
		raise PermissionDenied

	if deal.status == WholesaleDeal.PENDING:
		deal.status = WholesaleDeal.REJECTED
		deal.save()

	return redirect("deals:wholesale_deal_detail", pk)


class RetailDealForm(forms.ModelForm):
	"""Form definition for RetailDeal.

	Form for retail deal creation. Requires the primary
	key of the car involved in the retail deal to set the queryset.

	Parameters:
	car_pk (int): The primary key of the car involved in the deal
	"""

	class Meta:
		model = RetailDeal
		fields = ("car", "asking_price")

	def __init__(self, car_pk, *args, **kwargs):
		"""
		Constructor for Retail deal form.

		Sets the car field queryset to show only the car involved in the deal
		Sets the initial asking price to the car selling price (to encourage higher prices).

		"""
		
		super().__init__(*args, **kwargs)
		car_queryset = RetailCar.objects.filter(pk=car_pk)
		self.initial['car'] = car_queryset[0]
		self.initial['asking_price'] = car_queryset[0].retail_price
		self.fields['car'].queryset = car_queryset


class RetailDealCreateView(UserIsCustomer, CreateView):
	""" Create view to initialize a Retail deal."""

	template_name = "retail_deal_create.html"
	form_class = RetailDealForm

	def get_form(self):
		car_pk = self.kwargs.get("pk")
		return RetailDealForm(car_pk, **self.get_form_kwargs())

	def form_valid(self, form):
		""" Creates the deal or displays an error if customer balance is low. """
		total_cost = form.instance.asking_price
		if self.request.user.balance < total_cost:
			form.add_error(field=None, error="Your balance is too low")
			return self.form_invalid(form)
		form.instance.customer = self.request.user
		deal = form.save()

		dealership_admin = form.instance.car.dealership.admin
		assign_perm("view_retaildeal", self.request.user, deal)
		assign_perm("view_retaildeal", dealership_admin, deal)
		assign_perm("change_retaildeal", dealership_admin, deal)

		return super().form_valid(form)


class RetailDealDetailView(PermissionRequiredMixin, DetailView):
	""" Detail view for Retail deals. """
	model = RetailDeal
	template_name = "retail_deal_detail.html"
	context_object_name = "deal"

	permission_required = "view_retaildeal"
	raise_exception = True


@login_required
@transaction.atomic
def acceptRetailDeal(request, pk):
	""" View to accept a retail deal

	This view deducts the total price of the deal from the customer
	balance and adds it to the dealership's balance.
	It also deducts the amount of retail cars specified in the deal
	from the manufacturer's inventory.
	The deal status is updated to accepted

	Parameters:
		request (WSGI request): current request instance
		pk (int): primary key of retail deal

	Redirects to the retail deal detail view
	"""

	deal = RetailDeal.objects.get(pk=pk)
	dealership = deal.car.dealership

	if not dealership.admin.has_perm("change_retaildeal", deal):
		raise PermissionDenied
	total_cost = deal.asking_price
	customer_balance = deal.customer.balance
	if deal.status == RetailDeal.PENDING and customer_balance >= total_cost:

		deal.customer.balance = F('balance') - total_cost
		deal.customer.save()

		dealership.balance = F('balance') + total_cost
		dealership.save()

		deal.car.amount = F('amount') - deal.amount
		deal.car.save()

		deal.status = RetailDeal.ACCEPTED
		deal.save()

		return redirect("deals:retail_deal_detail", pk)
	else:
		return redirect("deals:retail_deal_detail", pk)


@login_required
def rejectRetailDeal(request, pk):
	""" View to reject a retail deal.

	Parameters:
		request (WSGI request): current request instance
		pk (int): primary key of retail deal


	This view sets the deal status to REJECTED.
	Redirects to the retail deal detail view.
	"""

	deal = RetailDeal.objects.get(pk=pk)
	dealership = deal.car.dealership
	
	if not dealership.admin.has_perm("change_retaildeal", deal):
		raise PermissionDenied
	
	if deal.status == RetailDeal.PENDING:
		deal.status = RetailDeal.REJECTED
		deal.save()

	return redirect("deals:retail_deal_detail", pk)




class ToManufacturersListView(UserIsDealership,ListView):
	model = WholesaleDeal
	template_name = "to_manufacturers.html"
	context_object_name = "deals"

	def get_queryset(self):
		return WholesaleDeal.objects.filter(dealership__admin=self.request.user)

class ToDealershipsListView(UserIsCustomer,ListView):
	model = RetailDeal
	template_name = "to_dealerships.html"
	context_object_name = "deals"

	def get_queryset(self):
		return RetailDeal.objects.filter(customer=self.request.user)