from .models import AccountStatement


def on_commit(sender, delta_x_info, receiver, amount, is_debit, description):
    deposit = AccountStatement()
    deposit.delta_x_info = delta_x_info
    deposit.sender = sender
    deposit.receiver = receiver
    deposit.amount = amount
    deposit.is_debit = is_debit
    deposit.description = description
    deposit.save()
    return deposit
