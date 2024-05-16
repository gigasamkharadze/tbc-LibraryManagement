from django.db.models import Count, F
from rest_framework.decorators import action as action_decorator
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from reservations.models import Reservation
from reservations.serializers import CreateReservationSerializer
from library.models import Book, Author, Genre
from library.pagination import BookPagination
from library.permissions import IsLibrarian, IsBorrower
from library.serializers import BookSerializer, AuthorSerializer, GenreSerializer


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    search_fields = ['title', 'author__first_name', 'author__last_name']
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['id', 'title', 'author__first_name', 'author__last_name', 'published_date']
    pagination_class = BookPagination

    def get_queryset(self):
        return Book.objects.all().select_related('author').prefetch_related('genre')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser, IsLibrarian]
        return [permission() for permission in permission_classes]

    @action_decorator(detail=False, methods=['get'], url_path='top-10')
    def top_10(self, request, *args, **kwargs):
        books = (Book.objects.all().
                 annotate(transactions_count=Count('transactions')).
                 order_by('-transactions_count')[:10])
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action_decorator(detail=False, methods=['get'], url_path='top-100-late-returned')
    def top_100_late_returned(self, request, *args, **kwargs):
        books = (Book.objects.all().
                 filter(transactions__return_date__isnull=False).
                 filter(transactions__return_date__gt=F('transactions__due_date')).
                 annotate(late_returned_count=Count('transactions')).
                 order_by('-late_returned_count')[:100])
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action_decorator(detail=True, methods=['get'], url_path='borrowed-count')
    def borrowed_count(self, request, *args, **kwargs):
        book = self.get_object()
        borrowed_count = book.transactions.count()
        return Response({'borrowed_count': borrowed_count})

    @action_decorator(detail=True, methods=['get'], url_path='top-100-late-returner-borrowers')
    def top_100_late_returner_borrowers(self, request, *args, **kwargs):
        book = self.get_object()
        borrowers = (book.transactions.
                     filter(return_date__isnull=False).
                     filter(return_date__gt=F('due_date')).
                     values('borrower').
                     annotate(late_returned_count=Count('borrower')).
                     order_by('-late_returned_count')[:100])
        return Response(borrowers)


class ReserveBookView(CreateModelMixin, GenericViewSet):
    queryset = Reservation.objects.all()
    serializer_class = CreateReservationSerializer
    permission_classes = [IsBorrower]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'book_id': self.kwargs['book_pk'],
            'request': self.request
        })
        return context

    @property
    def allowed_methods(self):
        return ['POST']
