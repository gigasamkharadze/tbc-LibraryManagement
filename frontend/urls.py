from django.urls import path
from frontend.views import home, login_view, register, logout_view, books, book, reserve_book


urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register-frontend'),
    path('logout/', logout_view, name='logout'),
    path('books/page/<int:page_number>/', books, name='books'),
    path('books/id/<int:book_id>/', book, name='book_detail'),
    path('books/id/<int:book_id>/reserve/', reserve_book, name='reserve-book'),
]
