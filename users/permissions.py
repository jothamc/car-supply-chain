"""
Permissions for everyobody YaaaY!!!."""

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin


class UserIsManufacturer(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.user_type == "MA"


class UserIsNotManufacturer(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.user_type != "MA"


def user_is_manufacturer(user):
    return user.is_authenticated and user.user_type == "MA"


class UserIsDealership(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.user_type == "DE"


class UserIsCustomer(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.user_type == "CU"


class UserIsNotCustomer(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.user_type != "CU"
