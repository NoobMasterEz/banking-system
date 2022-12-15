from rest_framework.permissions import IsAuthenticated


class IsBankOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.holder == request.user.customer
