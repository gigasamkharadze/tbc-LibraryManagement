from django.urls import path
from frontend.views import home, login_view


urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
]
