from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet

import users.models
from reservations.models import Reservation
from reservations.serializers import CreateReservationSerializer
from library.models import Book, Author, Genre
from library.pagination import BookPagination
from library.permissions import IsLibrarian, IsBorrower
from library.serializers import BookSerializer, AuthorSerializer, GenreSerializer, UpdateBookBorrowerSerializer


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


class ReserveBookView(
        CreateModelMixin,
        GenericViewSet):

    queryset = Reservation.objects.all()
    serializer_class = CreateReservationSerializer

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
