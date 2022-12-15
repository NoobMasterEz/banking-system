import factory

from delta_x.module.accounts.models import (AccountInformation,
                                            AccountStatement,
                                            generate_account_number)
from .users import CustomerFactory


class AccountInformationFactory(factory.django.DjangoModelFactory):
    guid = factory.Faker('uuid4')
    account_number = factory.LazyFunction(lambda: generate_account_number())
    holder = factory.RelatedFactory(CustomerFactory, 'accountinformation')
    is_active = True
    balance = factory.Faker('pyint', min_value=1, max_value=2000)

    class Meta:
        model = AccountInformation


class AccountStatementFactory(factory.django.DjangoModelFactory):
    delta_x_info = factory.SubFactory(AccountInformationFactory)
    sender = factory.SubFactory(CustomerFactory)
    receiver = factory.SubFactory(CustomerFactory)
    amount = factory.Faker('pyint', min_value=0, max_value=10000000)
    is_debit = True
    description = factory.Sequence(lambda n: f"test_{n}")

    class Meta:
        model = AccountStatement
