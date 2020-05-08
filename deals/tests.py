from django.test import TestCase
from django.urls import reverse
from guardian.shortcuts import assign_perm

from dealerships.models import Dealership
from inventory.models import RetailCar, WholesaleCar
from manufacturers.models import Manufacturer
from users.models import User

from .models import RetailDeal, WholesaleDeal

# Create your tests here.


class WholesaleDealTestCase(TestCase):
    def setUp(self):
        self.manu_admin = User.objects.create(
            username="manu_admin", user_type=User.MANUFACTURER)
        self.dealer_admin = User.objects.create(
            username="dealer_admin", user_type=User.DEALERSHIP)
        self.customer = User.objects.create(
            username="customer", user_type=User.CUSTOMER)
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", balance=0, admin=self.manu_admin)
        self.dealership = Dealership.objects.create(
            name="Test Dealership", balance=20000, admin=self.dealer_admin)

        self.w_car = WholesaleCar.objects.create(
            name="Model-100", amount=30, manufacturer=manufacturer, wholesale_price=2000)
        self.r_car = RetailCar.objects.create(
            name="Model-100", amount=30, dealership=self.dealership, retail_price=2000)

    def test_wholesale_deal_create(self):
        self.client.force_login(self.dealer_admin)
        response = self.client.get(
            reverse("deals:wholesale_deal_create", kwargs={"pk": self.w_car.pk}))
        self.assertEqual(response.status_code, 200)
        initial = response.context_data["form"].initial
        obj = WholesaleCar.objects.get(pk=self.w_car.pk)
        self.assertEqual(initial['car'], obj)
        self.assertEqual(initial['asking_price'], obj.wholesale_price)

        # Create deal.
        post_response = self.client.post(reverse("deals:wholesale_deal_create", kwargs={"pk": self.w_car.pk}), data={
            "car": self.w_car.pk,
            "amount": 3,
            "asking_price": 10000,
        })
        self.assertEqual(post_response.status_code, 302)
        # self.assertRedirects(post_response, reverse("deals:wholesale_deal_detail", kwargs={"pk":1}))

        # Check that it reflects on manufacturer page
        self.client.force_login(self.manu_admin)
        response = self.client.get(reverse("deals:from_dealerships"))
        self.assertContains(response, "Status: PENDING")
        self.assertContains(response, "Dealership: <b>Test Dealership</b>")

    def test_wholesale_deal_create_on_low_balance(self):
        self.client.force_login(self.dealer_admin)
        post_response = self.client.post(reverse("deals:wholesale_deal_create", kwargs={"pk": self.w_car.pk}), data={
            "car": self.w_car.pk,
            "amount": 3,
            "asking_price": 100000,
        })
        self.assertContains(post_response, "Your balance is too low")

    def test_accept_wholesale_deal(self):
        wd = WholesaleDeal.objects.create(car=self.w_car, asking_price=5000, amount=5,
                                          dealership=self.dealership)
        assign_perm("view_wholesaledeal", self.manu_admin, wd)
        assign_perm("change_wholesaledeal", self.manu_admin, wd)
        self.client.force_login(self.manu_admin)
        response = self.client.get(
            reverse("deals:wholesale_deal_accept", kwargs={"pk": wd.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "deals:wholesale_deal_detail", kwargs={"pk": wd.pk}))
        redirect_response = self.client.get(response.url)
        self.assertContains(redirect_response, "Status: ACCEPTED")

        # Check the manufacturer's balance
        new_response = self.client.get(reverse("user:profile"))
        self.assertContains(new_response, "Balance: $5,000")

        # Check the dealership balance
        self.client.force_login(self.dealer_admin)
        new_response = self.client.get(reverse("user:profile"))
        self.assertContains(new_response, "Balance: $15,000")

    def test_reject_wholesale_deal(self):
        wd = WholesaleDeal.objects.create(car=self.w_car, asking_price=5000, amount=5,
                                          dealership=self.dealership)
        assign_perm("view_wholesaledeal", self.manu_admin, wd)
        assign_perm("change_wholesaledeal", self.manu_admin, wd)
        self.client.force_login(self.manu_admin)
        response = self.client.get(
            reverse("deals:wholesale_deal_reject", kwargs={"pk": wd.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "deals:wholesale_deal_detail", kwargs={"pk": wd.pk}))
        redirect_response = self.client.get(response.url)
        self.assertContains(redirect_response, "Status: REJECTED")

    def test_others_wholesale_deal_create(self):
        self.client.force_login(self.manu_admin)
        response = self.client.get(
            reverse("deals:wholesale_deal_create", kwargs={"pk": self.w_car.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(
            reverse("deals:wholesale_deal_create", kwargs={"pk": self.w_car.pk}))
        self.assertEqual(post_response.status_code, 403)

        self.client.force_login(self.customer)
        response = self.client.get(
            reverse("deals:wholesale_deal_create", kwargs={"pk": self.w_car.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(
            reverse("deals:wholesale_deal_create", kwargs={"pk": self.w_car.pk}))
        self.assertEqual(post_response.status_code, 403)

    def test_others_wholesale_deal_detail(self):
        wd = WholesaleDeal.objects.create(car=self.w_car, asking_price=5000, amount=5,
                                          dealership=self.dealership)
        # Same manufacturer in the wholesale deal
        assign_perm("view_wholesaledeal", self.manu_admin, wd)
        self.client.force_login(self.manu_admin)
        response = self.client.get(
            reverse("deals:wholesale_deal_detail", kwargs={"pk": wd.pk}))
        self.assertEqual(response.status_code, 200)

        self.client.force_login(self.customer)
        response = self.client.get(
            reverse("deals:wholesale_deal_detail", kwargs={"pk": wd.pk}))
        self.assertEqual(response.status_code, 403)


####################################################


class RetailCarTestCase(TestCase):
    def setUp(self):
        self.manu_admin = User.objects.create(
            username="manu_admin", user_type=User.MANUFACTURER)
        self.dealer_admin = User.objects.create(
            username="dealer_admin", user_type=User.DEALERSHIP)
        self.customer = User.objects.create(
            username="customer", user_type=User.CUSTOMER, balance=30000)
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", balance=0, admin=self.manu_admin)
        dealership = Dealership.objects.create(
            name="Test Dealership", balance=0, admin=self.dealer_admin)

        self.w_car = WholesaleCar.objects.create(
            name="Model-100", amount=30, manufacturer=manufacturer, wholesale_price=2000)
        self.r_car = RetailCar.objects.create(
            name="Model-100", amount=30, dealership=dealership, retail_price=2000)

    def test_others_retail_deal_create(self):
        self.client.force_login(self.manu_admin)
        response = self.client.get(
            reverse("deals:retail_deal_create", kwargs={"pk": self.r_car.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(
            reverse("deals:retail_deal_create", kwargs={"pk": self.r_car.pk}))
        self.assertEqual(post_response.status_code, 403)

        self.client.force_login(self.dealer_admin)
        response = self.client.get(
            reverse("deals:retail_deal_create", kwargs={"pk": self.r_car.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(
            reverse("deals:retail_deal_create", kwargs={"pk": self.r_car.pk}))
        self.assertEqual(post_response.status_code, 403)

    def test_retail_deal_create(self):
        self.client.force_login(self.customer)
        response = self.client.get(
            reverse("deals:retail_deal_create", kwargs={"pk": self.r_car.pk}))
        self.assertEqual(response.status_code, 200)
        initial = response.context_data["form"].initial
        obj = RetailCar.objects.get(pk=self.r_car.pk)
        self.assertEqual(initial['car'], obj)
        self.assertEqual(initial['asking_price'], obj.retail_price)

        # Create deal.
        post_response = self.client.post(reverse("deals:retail_deal_create", kwargs={"pk": self.r_car.pk}), data={
            "car": self.r_car.pk,
            "asking_price": 10000,
        })
        self.assertEqual(post_response.status_code, 302)
        # self.assertRedirects(post_response, reverse("deals:retail_deal_detail", kwargs={"pk":}))

        # Check that it reflects on manufacturer page
        self.client.force_login(self.dealer_admin)
        response = self.client.get(reverse("deals:from_customers"))
        self.assertContains(response, "Status: PENDING")
        self.assertContains(response, "Customer: <b>customer</b>")

    def test_retail_deal_create_on_low_balance(self):
        self.client.force_login(self.customer)
        post_response = self.client.post(reverse("deals:retail_deal_create", kwargs={"pk": self.r_car.pk}), data={
            "car": self.r_car.pk,
            "asking_price": 100000,
        })
        self.assertContains(post_response, "Your balance is too low")

    def test_accept_retail_deal(self):
        rd = RetailDeal.objects.create(car=self.r_car, asking_price=5000, amount=5,
                                       customer=self.customer)
        assign_perm("view_retaildeal",self.dealer_admin, rd)
        assign_perm("change_retaildeal",self.dealer_admin, rd)
        self.client.force_login(self.dealer_admin)
        response = self.client.get(
            reverse("deals:retail_deal_accept", kwargs={"pk": rd.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "deals:retail_deal_detail", kwargs={"pk": rd.pk}))
        redirect_response = self.client.get(response.url)
        self.assertContains(redirect_response, "Status: ACCEPTED")

        # Check the dealerships's balance
        new_response = self.client.get(reverse("user:profile"))
        self.assertContains(new_response, "Balance: $5,000")

        # Check the customer's balance
        self.client.force_login(self.customer)
        new_response = self.client.get(reverse("user:profile"))
        self.assertContains(new_response, "Balance: $25,000")

    def test_reject_retail_deal(self):
        rd = RetailDeal.objects.create(car=self.r_car, asking_price=5000, amount=5,
                                       customer=self.customer)
        assign_perm("view_retaildeal",self.dealer_admin, rd)
        assign_perm("change_retaildeal",self.dealer_admin, rd)
        self.client.force_login(self.dealer_admin)
        response = self.client.get(
            reverse("deals:retail_deal_reject", kwargs={"pk": rd.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "deals:retail_deal_detail", kwargs={"pk": rd.pk}))
        redirect_response = self.client.get(response.url)
        self.assertContains(redirect_response, "Status: REJECTED")

    def test_others_retail_deal_detail(self):
        rd = RetailDeal.objects.create(car=self.r_car, asking_price=5000, amount=5,
                                       customer=self.customer)
        # Same dealership in the retail deal
        assign_perm("view_retaildeal", self.dealer_admin, rd)
        self.client.force_login(self.dealer_admin)
        response = self.client.get(
            reverse("deals:retail_deal_detail", kwargs={"pk": rd.pk}))
        self.assertEqual(response.status_code, 200)

        self.client.force_login(self.manu_admin)
        response = self.client.get(
            reverse("deals:retail_deal_detail", kwargs={"pk": rd.pk}))
        self.assertEqual(response.status_code, 403)
