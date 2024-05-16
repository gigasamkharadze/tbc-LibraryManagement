from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from library.views import AuthorViewSet, GenreViewSet, BookViewSet, ReserveBookView, top_100_late_returner_borrowers
from django.urls import path

router = DefaultRouter()
router.register('books', BookViewSet, basename='books')
router.register('genres', GenreViewSet, basename='genres')
router.register('authors', AuthorViewSet, basename='authors')

books_router = routers.NestedDefaultRouter(router, 'books', lookup='book')
books_router.register('reserve', ReserveBookView, basename='book-reserve')

urlpatterns = [
    path('top-100-late-returner-borrowers/', top_100_late_returner_borrowers, name='top-100-late-returner-borrowers'),
]

urlpatterns = urlpatterns + router.urls + books_router.urls
