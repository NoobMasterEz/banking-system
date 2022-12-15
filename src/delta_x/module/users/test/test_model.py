from django.test import TestCase
from django.urls import reverse

from factories.module.users import UserFactory, CustomerFactory


class TestUserModels(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_get_absolute_url_return_correct(self):
        assert self.user.get_absolute_url() == reverse('user-detail', kwargs={'pk': self.user.pk})

    def test_get_full_name_return_correct(self):
        assert self.user.get_full_name() == "%s %s" % (
            self.user.first_name,
            self.user.last_name)


class TestCustomerModels(TestCase):
    def setUp(self):
        self.customer = CustomerFactory()

    def test_get_absolute_url_return_correct(self):
        assert self.customer.get_absolute_url() == reverse('customer-detail', kwargs={'pk': self.customer.pk})

    def test_get_full_name_return_correct(self):
        assert self.customer.get_full_name() == "%s %s" % (
            self.customer.user.first_name,
            self.customer.user.last_name)
