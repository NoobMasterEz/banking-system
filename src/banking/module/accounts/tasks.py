from .models import AccountStatement


def on_commit(sender, banking_info, receiver, amount, is_debit, description):
    deposit = AccountStatement()
    deposit.banking_info = banking_info
    deposit.sender = sender
    deposit.receiver = receiver
    deposit.amount = amount
    deposit.is_debit = is_debit
    deposit.description = description
    deposit.save()
    return deposit
