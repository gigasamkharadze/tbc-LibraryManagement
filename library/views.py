from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet

import users.models
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
    search_fields = ['title', 'author__first_name', 'author__last_name']
    filter_backends = [SearchFilter, OrderingFilter]
    ordering_fields = ['id', 'title', 'author__first_name', 'author__last_name', 'published_date']
    pagination_class = BookPagination

    def get_queryset(self):
        return Book.objects.all().select_related('author').prefetch_related('genre')

    def get_serializer_class(self):
        if (self.action == 'partial_update' and
                self.request.user.is_authenticated and self.request.user.profile == users.models.User.UserProfile.BORROWER):
            return UpdateBookBorrowerSerializer
        return BookSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action == 'partial_update':
            permission_classes = [IsBorrower]
        else:
            permission_classes = [IsAdminUser, IsLibrarian]
        return [permission() for permission in permission_classes]
