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


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        personal_number = request.POST['personal_number']
        birth_date = request.POST['birth_date']
        response = requests.post('http://localhost:8000/api/users/register/', data={
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'personal_number': personal_number,
            'birth_date': birth_date,
        })
        if response.status_code == 201:
            return redirect('login')
        else:
            return render(request, 'frontend/register.html', {
                'error': response.json(),
            })
    return render(request, 'frontend/register.html')
