from django.test import TestCase
from django.urls import reverse

from .models import WholesaleCar, RetailCar
from manufacturers.models import Manufacturer
from dealerships.models import Dealership
from users.models import User
# Create your tests here.

class WholesaleCarTest(TestCase):
    """
    Tests to ascertain that manufacturer admins can access the appropriate cars
    and that the views act accordingly
    """
    def setUp(self):
        admin = User.objects.create(username="tester",user_type=User.MANUFACTURER)
        manufacturer1 = Manufacturer.objects.create(name="first",balance=2000000,admin=admin)
        manufacturer2 = Manufacturer.objects.create(name="second",balance=2000000)

        self.car1 = WholesaleCar.objects.create(
            name="car1",
            cost_price=2000,
            selling_price=2000,
            amount=12,
            manufacturer=manufacturer1,
        )

        car2 = WholesaleCar.objects.create(
            name="car1",
            cost_price=3000,
            selling_price=3000,
            amount=12,
            manufacturer=manufacturer2,
        )
        self.client.force_login(admin)


    def test_dealership_wholesale_list_view(self):
        dealership_admin = User.objects.create_user(username="customer",user_type=User.DEALERSHIP)
        self.client.force_login(dealership_admin)
        response = self.client.get(reverse("inventory:index"))
        self.assertTemplateUsed(response,"inventory/dealerships/inventory_list.html")
        
    def test_wholesale_list_view(self):
        response = self.client.get(reverse("inventory:index"))
        self.assertTemplateUsed(response,"inventory/manufacturers/inventory_list.html")
        self.assertContains(response,"Selling price per car: $2,000")
        self.assertNotContains(response, "Selling price per car: $3,000")

    def test_wholesale_detail_view(self):
        response = self.client.get(reverse("inventory:wholesale_detail", kwargs={"pk": self.car1.pk}))
        self.assertContains(response,"Car: car1")

    def test_manufacturer_wholesale_update_view(self):
        response = self.client.get(reverse("inventory:wholesale_update", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse("inventory:wholesale_update", kwargs={"pk": self.car1.pk}),
        data={
            "selling_price": 4000,
        })
        self.assertEqual(post_response.status_code, 302)
        new_response = self.client.get(post_response.url)
        self.assertContains(new_response, "Selling price: $4,000")
        

    def test_manufacturer_wholesale_delete_view(self):
        response = self.client.get(reverse("inventory:wholesale_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse("inventory:wholesale_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, reverse("inventory:index"))
        


class WrongManufacturerWholesaleCarTest(TestCase):
    """
    Tests to ascertain that other manufacturer admins cannot
    access cars that are not theirs
    """
    def setUp(self):
        admin = User.objects.create(username="tester",user_type=User.MANUFACTURER)
        wrong_admin = User.objects.create(username="tester1",user_type=User.MANUFACTURER)
        manufacturer1 = Manufacturer.objects.create(name="first",balance=2000000,admin=admin)

        self.car1 = WholesaleCar.objects.create(
            name="car1",
            cost_price=2000,
            selling_price=2000,
            amount=12,
            manufacturer=manufacturer1,
        )

        self.client.force_login(wrong_admin)


    def test_wrong_manufacturer_wholesale_detail_view(self):
        response = self.client.get(reverse("inventory:wholesale_detail", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_wrong_manufacturer_wholesale_update_view(self):
        response = self.client.get(reverse("inventory:wholesale_update", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(reverse("inventory:wholesale_update", kwargs={"pk": self.car1.pk}),
        data={
            "selling_price": 4000,
        })
        self.assertEqual(post_response.status_code, 403)
        

    def test_wrong_manufacturer_wholesale_delete_view(self):
        response = self.client.get(reverse("inventory:wholesale_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(reverse("inventory:wholesale_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(post_response.status_code, 403)
        



class OtherUserTypesWholesaleCarTest(TestCase):
    """
    Tests to ascertain dealership admins and customers
    cannot access wholesale cars
    """
    def setUp(self):
        admin = User.objects.create(username="tester",user_type=User.MANUFACTURER)
        manufacturer1 = Manufacturer.objects.create(name="first",balance=2000000,admin=admin)
        self.car1 = WholesaleCar.objects.create(
            name="car1",
            cost_price=2000,
            selling_price=2000,
            amount=12,
            manufacturer=manufacturer1,
        )
        self.client.force_login(admin)

    def test_not_manufacturer_wholesale_detail_view(self):
        # Test dealership and customer
        dealership_admin = User.objects.create_user(username="dealer",user_type=User.DEALERSHIP)
        self.client.force_login(dealership_admin)
        response = self.client.get(reverse("inventory:wholesale_detail", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)
        
        customer = User.objects.create_user(username="customer",user_type=User.CUSTOMER)
        self.client.force_login(customer)
        response = self.client.get(reverse("inventory:wholesale_detail", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_not_manufacturer_wholesale_update_view(self):
        # Test dealership and customer
        dealership_admin = User.objects.create_user(username="dealer",user_type=User.DEALERSHIP)
        self.client.force_login(dealership_admin)
        response = self.client.get(reverse("inventory:wholesale_update", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(reverse("inventory:wholesale_update", kwargs={"pk": self.car1.pk}))
        self.assertEqual(post_response.status_code, 403)
        
        customer = User.objects.create_user(username="customer",user_type=User.CUSTOMER)
        self.client.force_login(customer)
        response = self.client.get(reverse("inventory:wholesale_update", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(reverse("inventory:wholesale_update", kwargs={"pk": self.car1.pk}))
        self.assertEqual(post_response.status_code, 403)

    def test_not_manufacturer_wholesale_delete_view(self):
        # Test dealership and customer
        dealership_admin = User.objects.create_user(username="dealer",user_type=User.DEALERSHIP)
        self.client.force_login(dealership_admin)
        response = self.client.get(reverse("inventory:wholesale_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(reverse("inventory:wholesale_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(post_response.status_code, 403)
        
        customer = User.objects.create_user(username="customer",user_type=User.CUSTOMER)
        self.client.force_login(customer)
        response = self.client.get(reverse("inventory:wholesale_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(reverse("inventory:wholesale_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(post_response.status_code, 403)


###########################################


class RetailCarTest(TestCase):
    """
    Tests to ascertain that dealership admins can access the appropriate cars
    and that the views act accordingly
    """
    def setUp(self):
        admin = User.objects.create(username="tester",user_type=User.DEALERSHIP)
        dealership1 = Dealership.objects.create(name="first_dealership",balance=2000000,admin=admin)
        dealership2 = Dealership.objects.create(name="second_dealership",balance=2000000)

        manufacturer1 = Manufacturer.objects.create(name="first_manufacturer",balance=2000000)
        manufacturer2 = Manufacturer.objects.create(name="second_manufacturer",balance=2000000)


        self.car1 = RetailCar.objects.create(
            name="car1",
            cost_price=2000,
            selling_price=2000,
            amount=12,
            dealership=dealership1,
            manufacturer=manufacturer1,
        )

        car2 = RetailCar.objects.create(
            name="car1",
            cost_price=3000,
            selling_price=3000,
            amount=12,
            dealership=dealership2,
            manufacturer=manufacturer2,
        )
        self.client.force_login(admin)


    def test_manufacturer_wholesale_list_view(self):
        manufacturer_admin = User.objects.create_user(username="manu",user_type=User.MANUFACTURER)
        self.client.force_login(manufacturer_admin)
        response = self.client.get(reverse("inventory:index"))
        self.assertTemplateUsed(response,"inventory/manufacturers/inventory_list.html")
        
    def test_dealership_list_view(self):
        response = self.client.get(reverse("inventory:index"))
        self.assertTemplateUsed(response,"inventory/dealerships/inventory_list.html")
        self.assertContains(response,"Selling price per car: $2,000")
        self.assertNotContains(response, "Selling price per car: $3,000")

    def test_retail_detail_view(self):
        response = self.client.get(reverse("inventory:retail_detail", kwargs={"pk": self.car1.pk}))
        self.assertContains(response,"Car: car1")

    def test_dealership_retail_update_view(self):
        response = self.client.get(reverse("inventory:retail_update", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse("inventory:retail_update", kwargs={"pk": self.car1.pk}),
        data={
            "selling_price": 4000,
        })
        self.assertEqual(post_response.status_code, 302)
        new_response = self.client.get(post_response.url)
        self.assertContains(new_response, "Selling price: $4,000")
        

    def test_dealership_retail_delete_view(self):
        response = self.client.get(reverse("inventory:retail_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 200)
        post_response = self.client.post(reverse("inventory:retail_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(post_response.status_code, 302)
        self.assertRedirects(post_response, reverse("inventory:index"))
        


class WrongDealershipWholesaleCarTest(TestCase):
    """
    Tests to ascertain that other dealership admins cannot
    access cars that are not theirs
    """
    def setUp(self):
        admin = User.objects.create(username="tester",user_type=User.DEALERSHIP)
        wrong_admin = User.objects.create(username="tester1",user_type=User.DEALERSHIP)
        dealership1 = Dealership.objects.create(name="first",balance=2000000,admin=admin)

        self.car1 = RetailCar.objects.create(
            name="car1",
            cost_price=2000,
            selling_price=2000,
            amount=12,
            dealership=dealership1,
        )

        self.client.force_login(wrong_admin)


    def test_wrong_dealership_retail_detail_view(self):
        response = self.client.get(reverse("inventory:retail_detail", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_wrong_dealership_retail_update_view(self):
        response = self.client.get(reverse("inventory:retail_update", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(reverse("inventory:retail_update", kwargs={"pk": self.car1.pk}),
        data={
            "selling_price": 4000,
        })
        self.assertEqual(post_response.status_code, 403)
        

    def test_wrong_dealership_retail_delete_view(self):
        response = self.client.get(reverse("inventory:retail_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(reverse("inventory:retail_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(post_response.status_code, 403)
        



class OtherUserTypesRetailCarTest(TestCase):
    """
    Tests to ascertain manufacturer admins and customers
    cannot access retail cars
    """
    def setUp(self):
        admin = User.objects.create(username="tester",user_type=User.DEALERSHIP)
        dealership1 = Dealership.objects.create(name="first",balance=2000000,admin=admin)
        self.car1 = RetailCar.objects.create(
            name="car1",
            cost_price=2000,
            selling_price=2000,
            amount=12,
            dealership=dealership1,
        )
        self.client.force_login(admin)

    def test_not_dealership_retail_detail_view(self):
        # Test manufacturer and customer
        manufacturer_admin = User.objects.create_user(username="dealer",user_type=User.MANUFACTURER)
        self.client.force_login(manufacturer_admin)
        response = self.client.get(reverse("inventory:retail_detail", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)
        
        customer = User.objects.create_user(username="customer",user_type=User.CUSTOMER)
        self.client.force_login(customer)
        response = self.client.get(reverse("inventory:retail_detail", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)

    def test_not_dealership_retail_update_view(self):
        # Test dealership and customer
        manufacturer_admin = User.objects.create_user(username="dealer",user_type=User.MANUFACTURER)
        self.client.force_login(manufacturer_admin)
        response = self.client.get(reverse("inventory:retail_update", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(reverse("inventory:retail_update", kwargs={"pk": self.car1.pk}))
        self.assertEqual(post_response.status_code, 403)
        
        customer = User.objects.create_user(username="customer",user_type=User.CUSTOMER)
        self.client.force_login(customer)
        response = self.client.get(reverse("inventory:retail_update", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(reverse("inventory:retail_update", kwargs={"pk": self.car1.pk}))
        self.assertEqual(post_response.status_code, 403)

    def test_not_dealership_retail_delete_view(self):
        # Test dealership and customer
        manufacturer_admin = User.objects.create_user(username="dealer",user_type=User.MANUFACTURER)
        self.client.force_login(manufacturer_admin)
        response = self.client.get(reverse("inventory:retail_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(reverse("inventory:retail_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(post_response.status_code, 403)
        
        customer = User.objects.create_user(username="customer",user_type=User.CUSTOMER)
        self.client.force_login(customer)
        response = self.client.get(reverse("inventory:retail_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(response.status_code, 403)
        post_response = self.client.post(reverse("inventory:retail_delete", kwargs={"pk": self.car1.pk}))
        self.assertEqual(post_response.status_code, 403)

