import random

from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,
                                   HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND)
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)

from delta_x.api.user_and_customer.views import UserViewSet, CustomerViewSet
from factories.module.users import CustomerFactory, UserFactory


class TestUserAPI(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.payload = {
            'first_name': 'test',
            'last_name': 'test',
            'address': 'test',
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'testing123',
        }

    def test_api_user_should_connect_200(self):
        request = self.factory.get(path=reverse('user-list'))
        force_authenticate(request, self.user)
        view = UserViewSet.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == HTTP_200_OK

    def test_api_user_post_with_out_login_and_create_user_should_HTTP_401_UNAUTHORIZED(self):
        request = self.factory.post(path=reverse('user-list'), data=self.payload)
        view = UserViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_api_user_post_login_and_create_user_should_connect_200(self):
        request = self.factory.post(path=reverse('user-list'), data=self.payload)
        force_authenticate(request, self.user)
        view = UserViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == HTTP_201_CREATED

    def test_api_user_post_login_and_create_user_should_connect_400_req(self):
        self.payload['username'] = ''
        request = self.factory.post(path=reverse('user-list'), data=self.payload)
        force_authenticate(request, self.user)
        view = UserViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {'username': [
            ErrorDetail(string='This field may not be blank.', code='blank')
        ]}

    def test_api_user_by_pk_should_connect_200(self):
        request = self.factory.get(path=reverse('user-detail', args=[self.user.pk]))
        force_authenticate(request, self.user)
        view = UserViewSet.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == HTTP_200_OK
        assert dict(response.data[0])['username'] == self.user.username


class TestCustomerAPI(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.customer = CustomerFactory()
        idi = random.randrange(
            1111111111111,
            9999999999999,
            13)
        user = UserFactory()
        self.payload = {'user': user.id,
                        'address': 'test',
                        'identity_number': idi,
                        'gender': "male"}

    def test_api_customer_login_authur_user_should_connect_404(self):
        user = UserFactory()
        request = self.factory.get(path=reverse('customer-list'))
        force_authenticate(request, user)
        view = CustomerViewSet.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == HTTP_404_NOT_FOUND
        assert dict(response.data) == {'error': 'you are not register customer.'}

    def test_api_customer_post_with_out_login_and_create_customer_should_HTTP_401_UNAUTHORIZED(self):
        request = self.factory.post(path=reverse('customer-list'), data=self.payload)
        view = CustomerViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_api_customer_post_login_and_create_customer_should_connect_200(self):
        request = self.factory.post(path=reverse('customer-list'), data=self.payload)
        force_authenticate(request, self.customer.user)
        view = CustomerViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == HTTP_201_CREATED

    def test_api_customer_post_login_and_create_customer_should_connect_400_error_detail(self):
        self.payload['identity_number'] = ''
        request = self.factory.post(path=reverse('customer-list'), data=self.payload)
        force_authenticate(request, self.customer.user)
        view = CustomerViewSet.as_view({'post': 'create'})
        response = view(request)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {'identity_number': [
            ErrorDetail(string='This field may not be blank.', code='blank')
        ]}

    def test_api_customer_by_pk_should_connect_200(self):
        request = self.factory.get(path=reverse('customer-detail', args=[self.customer.pk]))
        force_authenticate(request, self.customer.user)
        view = CustomerViewSet.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == HTTP_200_OK
