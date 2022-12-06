from django.test import TestCase

from factories.module.bank_info import AccountInformationFactory, AccountStatementFactory


class TestAccountInformation(TestCase):
    def setUp(self):
        self.accunt_info = AccountInformationFactory()
        self.account = AccountStatementFactory(
            banking_info=self.accunt_info,
            sender=self.accunt_info.holder)

    def test_total_balance_should_return_correct(self):
        assert self.accunt_info.total_balance == self.account.amount
        assert self.account.sender != self.account.receiver

    def test_banking_info_should_return_correct(self):
        assert self.account.banking_info == self.accunt_info
        assert self.account.sender == self.accunt_info.holder
        assert self.account.sender.id == self.accunt_info.holder.id