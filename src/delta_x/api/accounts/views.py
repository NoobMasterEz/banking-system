from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from delta_x.module.accounts.models import AccountInformation, AccountStatement
from .serializers import (
    AccountSerializer,
    DepositTransactionsSerializer,
    WithdrawTransactionsSerializer,
    TransferTransactionSerializer)
from delta_x.module.cores.permissions import IsBankOwner


class AccountViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    serializer_class = AccountSerializer
    queryset = AccountInformation.objects.filter(is_deleted=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(holder=self.request.user.customer)

    def list(self, request, *args, **kwargs):
        user = request.user
        if not self.request.user.username or getattr(self.request.user, 'customer', None):
            return Response({'Error': 'something worg.'}, status=status.HTTP_401_UNAUTHORIZED)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance=user.customer.accountinformation)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, permission_classes=[IsBankOwner])
    def activate(self, request, **kwargs):
        bank_info = self.get_queryset().first()
        bank_info.is_active = True
        bank_info.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, permission_classes=[IsBankOwner])
    def deactivate(self, request, **kwargs):
        bank_info = self.get_queryset().first()
        bank_info.is_active = False
        bank_info.save()
        return Response(status=status.HTTP_200_OK)


class DepositViewSet(
        mixins.CreateModelMixin,
        GenericViewSet):

    serializer_class = DepositTransactionsSerializer
    queryset = AccountStatement.objects.filter(is_deleted=False)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['sender'] = request.user.customer.pk
        serializer = self.get_serializer(data=data, context={'request': request})
        if serializer.is_valid():
            response = serializer.save()
            return Response(response, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class WithdrawViewSet(DepositViewSet):
    serializer_class = WithdrawTransactionsSerializer
    queryset = AccountStatement.objects.filter(is_deleted=False)


class TransferViewSet(DepositViewSet):
    serializer_class = TransferTransactionSerializer
    queryset = AccountStatement.objects.filter(is_deleted=False)
