from django.db import transaction
from rest_framework import serializers

from delta_x.module.accounts.models import AccountInformation, AccountStatement
from delta_x.module.users.models import Customer
from delta_x.module.accounts.tasks import on_commit


class AccountSerializer(serializers.ModelSerializer):
    holder = serializers.CharField(source='holder.user.get_full_name')
    balance = serializers.DecimalField(
        source='total_balance',
        decimal_places=2,
        max_digits=12,
    )

    class Meta:
        model = AccountInformation
        fields = '__all__'


class TransactionsSerializer(serializers.ModelSerializer):
    delta_x_info = serializers.CharField(source='delta_x_info.account_number')
    sender = serializers.CharField(source='sender.user.get_full_name')
    receiver = serializers.CharField(source='receiver.user.get_full_name')

    class Meta:
        model = AccountStatement
        fields = '__all__'


class DepositTransactionsSerializer(serializers.Serializer):
    sender = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.filter(is_deleted=False),)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate(self, attrs):
        sender = attrs.get('sender')
        if not sender.accountinformation.is_active:
            raise serializers.ValidationError({
                'sender': 'Bank account is blocked or inactive.'
            })
        return attrs

    def create(self, validated_data):
        sender = validated_data.get('sender')
        deposit_amount = validated_data.get('amount')
        deposit = on_commit(
            sender=sender,
            delta_x_info=sender.accountinformation,
            receiver=sender,
            amount=deposit_amount,
            is_debit=False,
            description='Amount deposit')
        serializer = TransactionsSerializer(instance=deposit)
        return serializer.data


class WithdrawTransactionsSerializer(DepositTransactionsSerializer):
    @transaction.atomic
    def create(self, validated_data):
        sender = validated_data.get('sender')
        deposit_amount = validated_data.get('amount')

        sender_bank = AccountInformation.objects.select_for_update().get(
            pk=sender.accountinformation.pk
        )
        if sender_bank.total_balance < deposit_amount:
            raise serializers.ValidationError({
                'amount': 'Insufficient funds.'
            })

        sender = validated_data.get('sender')
        deposit_amount = validated_data.get('amount')
        deposit = on_commit(
            sender=sender,
            delta_x_info=sender.accountinformation,
            receiver=sender,
            amount=deposit_amount,
            is_debit=True,
            description='Amount withdrawn')
        serializer = TransactionsSerializer(instance=deposit)
        return serializer.data


class TransferTransactionSerializer(DepositTransactionsSerializer):
    destination_account_number = serializers.CharField()

    @transaction.atomic
    def create(self, validated_data):
        sender = validated_data.get('sender')
        amount = validated_data.get('amount')
        account_number = validated_data.get('destination_account_number')

        # chekc accout is alive
        try:
            receiver_bank = AccountInformation.objects.select_for_update().get(
                account_number=account_number
            )
        except AccountInformation.DoesNotExist():
            raise serializers.ValidationError({
                'destination_account_number': 'Invalid account number.'
            })
        if not receiver_bank.is_active:
            raise serializers.ValidationError({
                'receiver': 'Bank account is blocked or inactive.'
            })

        if not sender.accountinformation.is_active:
            raise serializers.ValidationError({
                'sender': 'Bank account is blocked or inactive.'
            })

        # check amount in account
        sender_bank = AccountInformation.objects.select_for_update().get(
            pk=sender.accountinformation.pk
        )
        if sender_bank.total_balance < amount:
            raise serializers.ValidationError({
                'amount': 'Insufficient funds.'
            })

        statement_sender = on_commit(
            sender=sender,
            delta_x_info=sender.accountinformation,
            receiver=receiver_bank.holder,
            amount=amount,
            is_debit=True,
            description='Amount transferred')

        # deposit receiver
        on_commit(
            sender=sender,
            delta_x_info=receiver_bank,
            receiver=receiver_bank.holder,
            amount=amount,
            is_debit=True,
            description='Amount received')
        serializer = TransactionsSerializer(instance=statement_sender)
        return serializer.data
