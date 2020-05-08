from django.test import TestCase
from django.urls import reverse
from users.models import User
from manufacturers.models import Manufacturer
from .models import Car

from guardian.shortcuts import assign_perm
# Create your tests here.
class BlueprintCustomerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="customer",user_type="CU")
        self.car = Car.objects.create(name="nice", price=10000)
        self.client.force_login(self.user)
        super().setUp()

    def test_customer_create_blueprint(self):
        response = self.client.get(reverse("blueprints:create"))
        self.assertEqual(response.status_code,403)
        response = self.client.post(reverse("blueprints:create"))
        self.assertEqual(response.status_code,403)

    def test_customer_edit_blueprint(self):
        response = self.client.get(reverse("blueprints:edit",kwargs={"pk":self.car.pk}))
        self.assertEqual(response.status_code,403)
        response = self.client.post(reverse("blueprints:edit",kwargs={"pk":self.car.pk}))
        self.assertEqual(response.status_code,403)

    def test_customer_list_blueprint(self):
        response = self.client.get(reverse("blueprints:index"))
        self.assertEqual(response.status_code,403)

    def test_customer_detail_blueprint(self):
        response = self.client.get(reverse("blueprints:detail", kwargs={"pk":self.car.pk}))
        self.assertEqual(response.status_code,403)

    def test_customer_delete_blueprint(self):
        response = self.client.get(reverse("blueprints:delete", kwargs={"pk": self.car.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(reverse("blueprints:delete", kwargs={"pk": self.car.pk}))
        self.assertEqual(post_response.status_code, 403)

class BlueprintDealershipTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="dealer",user_type="DE")
        self.car = Car.objects.create(name="nice", price=10000)
        self.client.force_login(self.user)
        super().setUp()

    def test_dealership_create_blueprint(self):
        response = self.client.get(reverse("blueprints:create"))
        self.assertEqual(response.status_code,403)
        response = self.client.post(reverse("blueprints:create"))
        self.assertEqual(response.status_code,403)

    def test_dealership_edit_blueprint(self):
        response = self.client.get(reverse("blueprints:edit",kwargs={"pk":self.car.pk}))
        self.assertEqual(response.status_code,403)
        response = self.client.post(reverse("blueprints:edit",kwargs={"pk":self.car.pk}))
        self.assertEqual(response.status_code,403)

    def test_dealership_list_blueprint(self):
        response = self.client.get(reverse("blueprints:index"))
        self.assertEqual(response.status_code,403)

    def test_dealership_detail_blueprint(self):
        response = self.client.get(reverse("blueprints:detail", kwargs={"pk":self.car.pk}))
        self.assertEqual(response.status_code,403)

    def test_dealership_delete_blueprint(self):
        response = self.client.get(reverse("blueprints:delete", kwargs={"pk": self.car.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(reverse("blueprints:delete", kwargs={"pk": self.car.pk}))
        self.assertEqual(post_response.status_code, 403)
        

class BlueprintManufacturerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="manufact",user_type="MA")
        self.other_manufacturer = User.objects.create(username="other",user_type="MA")
        self.manufacturer = Manufacturer.objects.create(
            name="NaijaManufacturer", admin=self.user,country="NG"
        )
        self.car = Car.objects.create(name="nice", price=10000, manufacturer=self.manufacturer )
        assign_perm("change_car", self.user, self.car)
        self.client.force_login(self.user)
        super().setUp()

    def test_manufacturer_create_blueprint(self):
        response = self.client.get(reverse("blueprints:create"))
        self.assertEqual(response.status_code,200)

        response = self.client.post(reverse("blueprints:create"),data={
            "name": "Test Model",
            "price": "30000"
        })
        # Test for new input in response
        redirection = self.client.get(response.url)
        self.assertContains(redirection,"Name: Test Model")

    def test_manufacturer_edit_blueprint(self):
        response = self.client.get(reverse("blueprints:edit",kwargs={"pk":self.car.pk}))
        self.assertEqual(response.status_code,200)

        response = self.client.post(reverse("blueprints:edit",kwargs={"pk":self.car.pk}),
        data={
            "name":"Best car", 
            "price":"12300",
        })
        self.assertRedirects(response, reverse("blueprints:detail", kwargs={"pk":self.car.pk}))
        redirection = self.client.get(response.url)
        self.assertContains(redirection,"Name: Best car")

    def test_manufacturer_list_blueprint(self):
        response = self.client.get(reverse("blueprints:index"))
        self.assertEqual(response.status_code,200)

    def test_manufacturer_detail_blueprint(self):
        response = self.client.get(reverse("blueprints:detail", kwargs={"pk":self.car.pk}))
        self.assertEqual(response.status_code,200)

    def test_manufacturer_delete_blueprint(self):
        response = self.client.get(reverse("blueprints:delete", kwargs={"pk": self.car.pk}))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse("blueprints:delete", kwargs={"pk": self.car.pk}))
        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, reverse("blueprints:index"))
        




class BlueprintOtherManufacturerTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="manufact",user_type="MA")
        self.other_manufacturer = User.objects.create(username="other",user_type="MA")
        self.manufacturer = Manufacturer.objects.create(
            name="NaijaManufacturer", admin=self.user,country="NG"
        )
        self.car = Car.objects.create(name="nice", price=10000, manufacturer=self.manufacturer )
        self.client.force_login(self.other_manufacturer)
        super().setUp()

    def test_manufacturer_edit_blueprint(self):
        response = self.client.get(reverse("blueprints:edit",kwargs={"pk":self.car.pk}))
        self.assertEqual(response.status_code,403)

        response = self.client.post(reverse("blueprints:edit",kwargs={"pk":self.car.pk}),
        data={
            "name":"Best car", 
            "price":"12300",
        })
        self.assertEqual(response.status_code,403)

    def test_manufacturer_detail_blueprint(self):
        response = self.client.get(reverse("blueprints:detail", kwargs={"pk":self.car.pk}))
        self.assertEqual(response.status_code,403)

    def test_manufacturer_delete_blueprint(self):
        response = self.client.get(reverse("blueprints:delete", kwargs={"pk": self.car.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(reverse("blueprints:delete", kwargs={"pk": self.car.pk}))
        self.assertEqual(post_response.status_code, 403)
        

