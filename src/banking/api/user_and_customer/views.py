from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins, status
from rest_framework.response import Response


from banking.module.users.models import User, Customer
from .serializers import (UserSerializer, CustomerSerializer)
# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomerViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):
    queryset = Customer.objects.filter(is_deleted=False).order_by('-created')
    serializer_class = CustomerSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        user = request.user
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        if not user.username:
            return Response({'error': 'you are not auth.'}, status=status.HTTP_401_UNAUTHORIZED)
        if not hasattr(user, 'customer'):
            return Response({'error': 'you are not register customer.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance=user.customer)
        return Response(serializer.data)
