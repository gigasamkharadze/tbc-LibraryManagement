from django.urls import path
from frontend.views import home, login_view, register, logout_view, books, book


urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register-frontend'),
    path('logout/', logout_view, name='logout'),
    path('books/', books, name='books'),
    path('books/<int:book_id>/', book, name='book'),
]
