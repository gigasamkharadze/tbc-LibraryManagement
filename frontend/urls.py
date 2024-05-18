from django.urls import path
from frontend.views import home, login_view, register


urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register-frontend'),
]
