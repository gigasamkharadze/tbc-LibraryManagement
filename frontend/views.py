from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse


def home(request):
    return render(request, 'frontend/home.html', {
        'user': request.user,
    })


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        response = requests.post('http://localhost:8000/api/token/', data={
            'email': email,
            'password': password,
        })
        if response.status_code == 200:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                request.session['refresh'] = response.json()['refresh']
                request.session['access'] = response.json()['access']
                return redirect('home')
        return render(request, 'frontend/login.html', {
            'error': 'Invalid username or password',
        })
    return render(request, 'frontend/login.html')
