from django.test import TestCase
from django.urls import reverse

from .models import User
from dealerships.models import Dealership
from manufacturers.models import Manufacturer

# Create your tests here.

class UserDetailViewTestCase(TestCase):

    def test_register_user(self):
        response = self.client.post(reverse("user:register"), data={
            "username": "testing",
            "password1": "testing_code_is_not_always_fun",
            "password2": "testing_code_is_not_always_fun",
            "user_type": "CU"
        })
        self.assertRedirects(response,reverse("user:profile"))

    def test_user_detail_view(self):
        user = User.objects.create(username="tester")
        self.client.force_login(user)
        response = self.client.get(reverse("user:profile"))
        self.assertContains(response,"Account: tester")
        self.assertContains(response,"Balance: $0")

    def test_customer_add_balance(self):
        user = User.objects.create(username="customer_tester",
            user_type=User.CUSTOMER)
        self.client.force_login(user)
        response = self.client.get(reverse("user:add_balance"))
        self.assertContains(response, "Customer name: customer_tester")
        self.assertContains(response, "Current balance: $0")
        
        response = self.client.post(reverse("user:add_balance"),data={
            "balance": 10000
        })
        redirection = response.url
        new_response = self.client.get(redirection)
        self.assertContains(new_response, "Balance: $10,000")

    def test_dealership_add_balance(self):
        user = User.objects.create(username="dealership_tester",
            user_type=User.DEALERSHIP)
        Dealership.objects.create(name="Dealer Motors", admin=user)
        self.client.force_login(user)
        response = self.client.get(reverse("user:add_balance"))
        self.assertContains(response, "Dealership name: Dealer Motors")
        self.assertContains(response, "Current balance: $0")
        
        response = self.client.post(reverse("user:add_balance"),data={
            "balance": 10000
        })
        redirection = response.url
        new_response = self.client.get(redirection)
        self.assertContains(new_response, "Balance: $10,000")

    def test_manufacturer_add_balance(self):
        user = User.objects.create(username="manufacturer_tester",
            user_type=User.MANUFACTURER)
        Manufacturer.objects.create(name="Naija Manufacturer", admin=user)
        self.client.force_login(user)
        response = self.client.get(reverse("user:add_balance"))
        self.assertContains(response, "Manufacturer name: Naija Manufacturer")
        self.assertContains(response, "Current balance: $0")
        
        response = self.client.post(reverse("user:add_balance"),data={
            "balance": 10000
        })
        redirection = response.url
        new_response = self.client.get(redirection)
        self.assertContains(new_response, "Balance: $10,000")



    def test_manufacturer_add_negative_balance(self):
        user = User.objects.create(username="manufacturer_tester",
            user_type=User.MANUFACTURER)
        Manufacturer.objects.create(name="Naija Manufacturer", admin=user, balance=10000)
        self.client.force_login(user)
        response = self.client.get(reverse("user:add_balance"))
        self.assertContains(response, "Manufacturer name: Naija Manufacturer")
        self.assertContains(response, "Current balance: $10,000")
        
        response = self.client.post(reverse("user:add_balance"),data={
            "balance": -9999
        })
        self.assertContains(response, "Ensure this value is greater than or equal to 0")


