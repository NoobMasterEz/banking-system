from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)

from banking.api.accounts.views import (AccountViewSet, DepositViewSet,
                                        TransferViewSet, WithdrawViewSet)
from factories.module.bank_info import (AccountInformationFactory,
                                        AccountStatementFactory)


class TestAccountViewSet(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.account = AccountInformationFactory()

    def test_api_account_should_connect_200(self):
        request = self.factory.get(path=reverse('account-list'))
        force_authenticate(request, self.account.holder.user)
        view = AccountViewSet.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == HTTP_200_OK

    def test_api_account_should_connect_401(self):
        request = self.factory.get(path=reverse('account-list'))
        view = AccountViewSet.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert dict(response.data) == {'error': 'you are not auth.'}

    def test_api_user_by_pk_should_connect_200(self):
        request = self.factory.get(path=reverse('account-detail', args=[self.account.holder.user.pk]))
        force_authenticate(request, self.account.holder.user)
        view = AccountViewSet.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == HTTP_200_OK
        assert dict(response.data)['holder'] == self.account.holder.user.get_full_name()


class TestDepositViewSet(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.account = AccountInformationFactory()
        self.payload = {
            "sender": self.account.holder.id,
            "amount": 300
        }

    def test_api_account_deposit_hould_connect_401(self):
        request = self.factory.post(path=reverse('deposit-list'), data=self.payload)
        view = DepositViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.data == {'detail':
                                 ErrorDetail(string='Authentication credentials were not provided.',
                                             code='not_authenticated')}

    def test_api_account_deposit_post_login_should_connect_200(self):
        request = self.factory.post(path=reverse('deposit-list'), data=self.payload)
        force_authenticate(request, self.account.holder.user)
        view = DepositViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == HTTP_201_CREATED

    def test_api_account_deposit_check_type_post_login_should_raise_invalid_connect_400(self):
        payload = {
            "sender": self.account.holder.id,
            "amount": hex(30)
        }
        request = self.factory.post(path=reverse('deposit-list'), data=payload)
        force_authenticate(request, self.account.holder.user)
        view = DepositViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {'amount': [
            ErrorDetail(string='A valid number is required.',
                        code='invalid')]}


class TestWithdrawViewSet(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.accunt_info = AccountInformationFactory()
        self.account = AccountStatementFactory(
            banking_info=self.accunt_info,
            sender=self.accunt_info.holder)
        self.payload = {
            "sender": self.accunt_info.holder.id,
            "amount": 300
        }

    def test_api_with_draw_hould_connect_401(self):
        request = self.factory.post(path=reverse('withdraw-list'), data=self.payload)
        view = WithdrawViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.data == {'detail':
                                 ErrorDetail(string='Authentication credentials were not provided.',
                                             code='not_authenticated')}

    def test_api_with_draw_post_login_should_connect_200(self):
        request = self.factory.post(path=reverse('withdraw-list'), data=self.payload)
        force_authenticate(request, self.accunt_info.holder.user)
        view = WithdrawViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == HTTP_201_CREATED

    def test_api_with_draw_check_type_post_login_should_raise_invalid_connect_400(self):
        payload = {
            "sender": self.accunt_info.holder.id,
            "amount": hex(30)
        }
        request = self.factory.post(path=reverse('withdraw-list'), data=payload)
        force_authenticate(request, self.accunt_info.holder.user)
        view = WithdrawViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {'amount': [
            ErrorDetail(string='A valid number is required.',
                        code='invalid')]}


class TestTransferViewSet(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.accunt_info = AccountInformationFactory()
        self.accunt_info_2 = AccountInformationFactory()
        self.account = AccountStatementFactory(
            banking_info=self.accunt_info,
            sender=self.accunt_info.holder)
        self.payload = {
            "sender": self.accunt_info.holder.id,
            "amount": 300,
            "destination_account_number": self.accunt_info_2.account_number
        }

    def test_api_transfer_hould_connect_401(self):
        request = self.factory.post(path=reverse('transfer-list'), data=self.payload)
        view = TransferViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == HTTP_401_UNAUTHORIZED
        assert response.data == {'detail':
                                 ErrorDetail(string='Authentication credentials were not provided.',
                                             code='not_authenticated')}

    def test_api_transfer_post_login_should_connect_200(self):
        request = self.factory.post(path=reverse('transfer-list'), data=self.payload)
        force_authenticate(request, self.accunt_info.holder.user)
        view = TransferViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == HTTP_201_CREATED

    def test_api_transfer_check_type_post_login_should_raise_invalid_connect_400(self):
        payload = {
            "sender": self.accunt_info.holder.id,
            "amount": hex(30),
            "destination_account_number": self.accunt_info_2.account_number
        }
        request = self.factory.post(path=reverse('transfer-list'), data=payload)
        force_authenticate(request, self.accunt_info.holder.user)
        view = TransferViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {'amount': [
            ErrorDetail(string='A valid number is required.',
                        code='invalid')]}
