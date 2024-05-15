from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser


from transactions.models import Transaction
from transactions.serializers import (CreateTransactionSerializer, UpdateTransactionSerializer,
                                      ListTransactionSerializer, RetrieveTransactionSerializer)
from library.permissions import IsLibrarian


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    permission_classes = [IsLibrarian, IsAdminUser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['book__title', 'user__username']
    ordering_fields = ['checkout_date', 'return_date']
    ordering = ['-checkout_date']

    def get_serializer_class(self):
        if self.action == 'list':
            return ListTransactionSerializer
        if self.action == 'update':
            return UpdateTransactionSerializer
        if self.action == 'retrieve':
            return RetrieveTransactionSerializer
        return CreateTransactionSerializer
