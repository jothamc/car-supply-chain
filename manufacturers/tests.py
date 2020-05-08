from django.test import TestCase
from django.urls import reverse

from users.models import User
from blueprints.models import Car
from .models import Manufacturer, ManufacturingOrder
# Create your tests here.

class ManufacturingOrderTest(TestCase):
    
    def setUp(self):
        # user = User.objects.create(username="tester",
        # user_type=User.MANUFACTURER)
        # self.client.force_login(user)
        user = User.objects.create(username="tester",
        user_type=User.MANUFACTURER)
        self.manufacturer = Manufacturer.objects.create(name="NaijaManufacturer",balance=1500000, 
        admin=user)
        self.blueprint = Car.objects.create(name="model-1", price=20000,
        manufacturer=self.manufacturer)
        self.client.force_login(user)




    def test_customer_manufacturing_order_create_view(self):
        user = User.objects.create(username="customer_tester",
        user_type=User.CUSTOMER)
        self.client.force_login(user)
        response = self.client.get(reverse("manufacturers:create"))
        self.assertEqual(response.status_code,403)

    def test_dealership_manufacturing_order_create(self):
        user = User.objects.create(username="dealership_tester",
        user_type=User.DEALERSHIP)
        self.client.force_login(user)
        response = self.client.get(reverse("manufacturers:create"))
        self.assertEqual(response.status_code,403)

    def test_manufacturer_manufacturing_order_create(self):
        response = self.client.get(reverse("manufacturers:create"))
        self.assertEqual(response.status_code,200)
        post_response = self.client.post(reverse("manufacturers:create"),data={
            "count": 10,
            "car": self.blueprint.pk
        })
        self.assertRedirects(post_response,reverse("manufacturers:mo_detail",kwargs={"pk":1}))
        last_response =self.client.get(reverse("user:profile"))
        self.assertContains(last_response, "Balance: $1,300,000")
 
    def test_manufacturer_manufacturing_order_create_fail(self):
        """
        Order more than balance
        """
        post_response = self.client.post(reverse("manufacturers:create"),data={
            "count": -100,
            "car": self.blueprint.pk
        })
        # print(post_response.content)
        self.assertContains(post_response,"Ensure this value is greater than or equal to 0")
        post_response = self.client.post(reverse("manufacturers:create"),data={
            "count": 100,
            "car": self.blueprint.pk
        })
        self.assertContains(post_response,"Your balance is too low")
