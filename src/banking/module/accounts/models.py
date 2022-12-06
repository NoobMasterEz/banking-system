import random
import uuid

from django.db import models
from django.db.models import Sum

from banking.module.cores.models import Info
from banking.module.users.models import Customer


def generate_account_number():
    return ''.join(random.choice('0123456789ABCDEFGH') for _ in range(13))


class AccountInformation(Info):
    guid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    account_number = models.CharField(max_length=15, unique=True, default=generate_account_number())
    holder = models.OneToOneField(Customer,
                                  on_delete=models.CASCADE,
                                  null=True,
                                  blank=True,
                                  related_name="accountinformation")
    is_active = models.BooleanField(default=True)
    balance = models.DecimalField(decimal_places=2,
                                  max_digits=12,
                                  default=0)

    def _total_is_none(self, aggregate):
        total = aggregate.get('total')
        return total if total else 0

    @property
    def total_balance(self):
        debit = AccountStatement.objects.filter(
            banking_info__pk=self.pk,
            is_debit=True,
        )
        credit = AccountStatement.objects.filter(
            banking_info__pk=self.pk,
            is_debit=False,
        )
        credit = self._total_is_none(credit.aggregate(total=Sum('amount')))
        debit = self._total_is_none(debit.aggregate(total=Sum('amount')))
        return abs(credit - debit)

    def __str__(self):
        return self.account_number


class AccountStatement(Info):
    guid = models.UUIDField(editable=False, default=uuid.uuid4)
    banking_info = models.ForeignKey(
        AccountInformation,
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        Customer,
        related_name='sender',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        Customer,
        related_name='receiver',
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    is_debit = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return (
            f'Owner:: {self.banking_info.holder.user.get_full_name()} '
            f'{"Debit: " if self.is_debit else "Credit:"} {self.amount}'
        )
