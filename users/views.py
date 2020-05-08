from django import forms
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, UpdateView

from dealerships.models import Dealership
from manufacturers.models import Manufacturer

from .models import User

# Create your views here.


class UserDetailView(LoginRequiredMixin, DetailView):
	"""
	Detail View for users.

	This view selects appropriate context data and templates for each user.

	"""

	model = User

	def get_object(self):
		return self.request.user

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)

		user_type = self.object.user_type
		if user_type == "MA":
			affiliation = self.object.manufacturer_set.get()
		elif user_type == "DE":
			affiliation = self.object.dealership_set.get()
		elif user_type == "CU":
			affiliation = self.object

		context["affiliation"] = affiliation
		return context

	def get_template_names(self):
		user_type = self.object.user_type
		if user_type == User.MANUFACTURER:
			template_name = "users/manufacturer_admin_detail.html"

		elif user_type == User.DEALERSHIP:
			template_name = "users/dealership_admin_detail.html"

		elif user_type == User.CUSTOMER:
			template_name = "users/customer_detail.html"

		return template_name


class CustomUserCreationForm(UserCreationForm):
	"""User creation form subcassed from Django's auth user creation form."""

	class Meta:
		model = User
		fields = UserCreationForm.Meta.fields + ('user_type',)


class RegisterView(CreateView):
	""" Create view for creating new users 

	All other users except customers must be associated to a dealership 
	or manufacturer via the admin panel or else they cannot access
	user detail view after registration.
	"""

	model = User
	form_class = CustomUserCreationForm
	template_name = "registration/register.html"

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect("user:profile")


class ManufacturerForm(forms.ModelForm):
	"""Form definition for Manufacturer balance increment."""

	class Meta:
		model = Manufacturer
		fields = ('balance',)
		widgets = {
			"balance": forms.TextInput(attrs={
				"type": "number",
				"min": 1
			})
		}


class DealershipForm(forms.ModelForm):
	"""Form definition for Dealership balance increment."""

	class Meta:
		model = Dealership
		fields = ('balance',)
		widgets = {
			"balance": forms.TextInput(attrs={
				"type": "number",
				"min": 1
			})
		}


class CustomerForm(forms.ModelForm):
	"""Form definition for Customer balance increment."""

	class Meta:
		model = User
		fields = ('balance',)
		widgets = {
			"balance": forms.TextInput(attrs={
				"type": "number",
				"min": 1
			})
		}


def chooseUserForm(user_type):
	if user_type == User.MANUFACTURER:
		return ManufacturerForm
	elif user_type == User.DEALERSHIP:
		return DealershipForm
	elif user_type == User.CUSTOMER:
		return CustomerForm


@login_required
def AddBalanceView(request):
	"""
	View to increase balance of user

	Receives input from form data and updates appropriate field.
	If user is manufacturer admin, Manufacturer balance is updated
	If user is dealership admin, Dealership balance is updated
	If user is customer, customer balance is updated

	Redirects to user detail view if successful
	"""

	template_name = "users/add-balance.html"
	user_type = request.user.user_type
	if request.method == "POST":
		form = chooseUserForm(user_type)
		form = form(request.POST)
		if form.is_valid():
			increment = form.instance.balance

			if user_type == User.MANUFACTURER:
				manufacturer = request.user.manufacturer_set.all()
				manufacturer.update(balance=F('balance') + increment)
			
			elif user_type == User.DEALERSHIP:
				dealership = request.user.dealership_set.all()
				dealership.update(balance=F('balance') + increment)
			
			elif user_type == User.CUSTOMER:
				customer = request.user
				customer.balance = F('balance') + increment
				customer.save()

			success_url = "user:profile"
			return redirect(success_url)
		else:
			return render(request, template_name, {"form": form})
	else:
		form = chooseUserForm(user_type)
		return render(request, template_name, {"form": form})
