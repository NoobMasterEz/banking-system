from django.test import TestCase
from rest_framework.exceptions import ErrorDetail

from delta_x.api.accounts.serializers import AccountSerializer, TransactionsSerializer


class TestAccountSerializer(TestCase):
    def setUp(self):
        self.data = {
            "holder": "test",
            "balance": 12,
        }

    def test_valid_account_serializer_should_no_have_errors_and_default_validators(self):
        serializer = AccountSerializer(
            data=self.data
        )
        assert serializer.is_valid()
        assert dict(serializer.validated_data) == {
            'holder': {
                'user': {
                    'get_full_name': 'test'
                }
            },
            'total_balance': 12.00
        }
        assert serializer.errors == {}
        assert serializer.default_validators == []

    def test_invalid_required_account_serializer(self):
        del self.data['balance']
        serializer = AccountSerializer(
            data=self.data
        )
        assert not serializer.is_valid()
        assert serializer.validated_data == {}
        assert serializer.errors == {
            'balance': [ErrorDetail(string='This field is required.', code='required')]
        }

    def test_invalid_account_serializer_datatype(self):
        serializer = AccountSerializer(
            data=list(self.data)
        )
        assert not serializer.is_valid()
        assert serializer.validated_data == {}
        assert serializer.errors == {
            'non_field_errors': [ErrorDetail(
                string='Invalid data. Expected a dictionary, but got list.',
                code='invalid')]
        }


class TestTransactionsSerializer(TestCase):
    def setUp(self):
        self.data = {
            "delta_x_info": "test",
            "sender": "test1",
            "receiver": "test1",
            "amount": 300,
        }

    def test_valid_transactions_serializer_should_no_have_errors_and_default_validators(self):
        serializer = TransactionsSerializer(
            data=self.data
        )
        assert serializer.is_valid()
        assert dict(serializer.validated_data) == {
            'delta_x_info': {
                'account_number': 'test'
            },
            'sender': {
                'user': {
                    'get_full_name': 'test1'
                }
            },
            'receiver': {
                'user': {
                    'get_full_name': 'test1'
                }
            },
            'amount': 300.00
        }
        assert serializer.errors == {}
        assert serializer.default_validators == []

    def test_invalid_required_transactions_serializer(self):
        del self.data['sender']
        serializer = TransactionsSerializer(
            data=self.data
        )
        assert not serializer.is_valid()
        assert serializer.validated_data == {}
        assert serializer.errors == {
            'sender': [ErrorDetail(string='This field is required.', code='required')]
        }

    def test_invalid_transactions_serializer_datatype(self):
        serializer = TransactionsSerializer(
            data=list(self.data)
        )
        assert not serializer.is_valid()
        assert serializer.validated_data == {}
        assert serializer.errors == {
            'non_field_errors': [ErrorDetail(
                string='Invalid data. Expected a dictionary, but got list.',
                code='invalid')]
        }
