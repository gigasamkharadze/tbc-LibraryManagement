from rest_framework.routers import DefaultRouter
from library.views import AuthorViewSet, GenreViewSet, BookViewSet

router = DefaultRouter()
router.register('books', BookViewSet, basename='books')
router.register('genres', GenreViewSet, basename='genres')
router.register('authors', AuthorViewSet, basename='authors')

urlpatterns = router.urls
