from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from library.views import AuthorViewSet, GenreViewSet, BookViewSet, ReserveBookView

router = DefaultRouter()
router.register('books', BookViewSet, basename='books')
router.register('genres', GenreViewSet, basename='genres')
router.register('authors', AuthorViewSet, basename='authors')

books_router = routers.NestedDefaultRouter(router, 'books', lookup='book')
books_router.register('reserve', ReserveBookView, basename='book-reserve')

urlpatterns = router.urls + books_router.urls
