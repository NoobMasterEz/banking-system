import factory
import random

from django.contrib.auth.hashers import make_password

from banking.module.users.models import Customer, User
from banking.module.cores import defult


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('email')
    password = factory.LazyFunction(lambda: make_password('pi3.1415'))

    class Meta:
        model = User


class CustomerFactory(factory.django.DjangoModelFactory):
    guid = factory.Faker('uuid4')
    address = factory.Sequence(lambda n: f"test_{n}")
    identity_number = factory.LazyFunction(lambda: random.randrange(
        1111111111111,
        9999999999999,
        13))
    user = factory.SubFactory(UserFactory)
    gender = factory.Faker(
        'random_element', elements=[x[0] for x in defult.SEX_CHOICES]
    )

    class Meta:
        model = Customer
