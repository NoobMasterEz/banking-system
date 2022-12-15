from django.test import TestCase
from rest_framework.exceptions import ErrorDetail

from delta_x.api.user_and_customer.serializers import UserSerializer, CustomerSerializer
from factories.module.users import UserFactory


class TestUserSerializer(TestCase):
    def setUp(self):
        self.data = {'email': 'test123@Gmail.com',
                     'username': 'test1',
                     'first_name': 'test2',
                     'last_name': 'test3'}

    def test_valid_user_serializer_should_no_have_errors_and_default_validators(self):
        serializer = UserSerializer(data=self.data)
        assert serializer.is_valid()
        assert dict(serializer.validated_data) == self.data
        assert serializer.errors == {}
        assert serializer.default_validators == []

    def test_invalid_required_user_serializer(self):
        del self.data['username']
        serializer = UserSerializer(
            data=self.data
        )
        assert not serializer.is_valid()
        assert serializer.validated_data == {}
        assert serializer.errors == {
            'username': [ErrorDetail(string='This field is required.', code='required')]
        }

    def test_invalid_user_serializer_datatype(self):
        serializer = UserSerializer(
            data=list(self.data)
        )
        assert not serializer.is_valid()
        assert serializer.validated_data == {}
        assert serializer.errors == {
            'non_field_errors': [ErrorDetail(
                string='Invalid data. Expected a dictionary, but got list.',
                code='invalid')]
        }


class TestCustomerSerializer(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.data = {'user': self.user.id,
                     'address': 'test1',
                     'identity_number': '1111111111111',
                     'gender': "male"}

    def test_valid_customer_serializer_should_no_have_errors_and_default_validators(self):
        serializer = CustomerSerializer(data=self.data)
        assert serializer.is_valid()
        self.data['user'] = self.user
        assert dict(serializer.validated_data) == self.data
        assert serializer.errors == {}
        assert serializer.default_validators == []

    def test_invalid_required_customer_serializer(self):
        del self.data['identity_number']
        serializer = CustomerSerializer(
            data=self.data
        )
        assert not serializer.is_valid()
        assert serializer.validated_data == {}
        assert serializer.errors == {
            'identity_number': [ErrorDetail(string='This field is required.', code='required')]
        }

    def test_invalid_customer_serializer_datatype(self):
        serializer = CustomerSerializer(
            data=str(self.data)
        )
        assert not serializer.is_valid()
        assert serializer.validated_data == {}
        assert serializer.errors == {
            'non_field_errors': [ErrorDetail(
                string='Invalid data. Expected a dictionary, but got str.',
                code='invalid')]
        }
