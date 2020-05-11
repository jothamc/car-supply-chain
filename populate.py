import json
import random

from blueprints.models import Car
from manufacturers.models import Manufacturer
from inventory.models import WholesaleCar
from users.models import User
from dealerships.models import Dealership

from guardian.shortcuts import assign_perm

with open("countries-django.json") as file:
    countries = json.loads(file.read())


def populate_cars(initial=True):
    with open("car-models.json") as file:
        cars = json.loads(file.read())

    for car in cars:

        brand = car['brand']
        country = random.choice(countries)[0]

        if initial:
            username = f"{brand}_admin".lower().replace(" ","_").replace("-","_")
            manufacturer_admin = User(
                username=username, user_type=User.MANUFACTURER)

            manufacturer_admin.set_password("admin")
            manufacturer_admin.save()

            manufacturer = Manufacturer.objects.create(
                name=brand, country=country, admin=manufacturer_admin)

            print(f"Created Manufacturer: {brand}")
            print(f"Manufacturer admin username: {username}")
            print(f"Manufacturer admin password: admin")
            print()
        
        else:
            manufacturer = Manufacturer.objects.get(name=brand)

        for model in car['models']:
            price = round(random.random() * 100) * 1000
            # name = f"{brand} {model}"

            car = Car.objects.create(name=model, price=price,
                               manufacturer=manufacturer)
            amount = price/1000
            w_car = WholesaleCar.objects.create(
                name=model, wholesale_price=price, cost_price=price, amount=amount, manufacturer=manufacturer)

            assign_perm("change_car", manufacturer.admin, car)
            assign_perm("change_wholesalecar", manufacturer.admin, w_car)


def populate_dealerships():
    names = "Andrew Jefferson Nicholas Smith Sydney Williams Samuel Robertson Jessica Price Jackson Kingston"
    split_names = names.split()

    for name in split_names:
        country = random.choice(countries)[0]
        dealership_name = f"{name} Motors"

        username = f"{name.lower()}_admin"
        dealership_admin = User(
            username=username, user_type=User.DEALERSHIP)
        dealership_admin.set_password("admin")
        dealership_admin.save()

        dealership = Dealership(
            name=dealership_name, country=country, admin=dealership_admin)
        dealership.save()

        print(f"Created Dealership: {dealership.name}")
        print(f"Dealership admin username: {username}")
        print(f"Dealership admin password: admin")
        print()


def populate_database():
    populate_cars()
    for _ in range(3):
        print(f"Duplicating all cars")
        populate_cars(initial=False)
    populate_dealerships()
    customer = User(username="customer", user_type=User.CUSTOMER)
    customer.set_password("customer")
    customer.save()
    print("Created Customer: customer")
    print("Customer username: customer")
    print("Customer password: customer")

