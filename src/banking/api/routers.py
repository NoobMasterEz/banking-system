from rest_framework import routers

from .user_and_customer.views import UserViewSet, CustomerViewSet
from .accounts.views import AccountViewSet, DepositViewSet, WithdrawViewSet, TransferViewSet

router = routers.DefaultRouter()
router.register('user', UserViewSet)
router.register('customer', CustomerViewSet)

router.register('account', AccountViewSet, basename='account')
router.register('deposit', DepositViewSet, basename='deposit')
router.register('withdraw', WithdrawViewSet, basename='withdraw')
router.register('transfer', TransferViewSet, basename='transfer')
