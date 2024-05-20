from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
import requests


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


def logout_view(request):
    if 'access' in request.session:
        del request.session['access']
    if 'refresh' in request.session:
        del request.session['refresh']
    logout(request)
    return redirect('home')


def books(request):
    if 'access' in request.session:
        headers = {'Authorization': f'Bearer {request.session["access"]}'}
        try:
            response = requests.get('http://localhost:8000/api/library/books/', headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            logout(request)
            return render(request, 'frontend/error.html', {
                'message': 'An error occurred while fetching books.'
            })

        if response.status_code == 200:
            all_books = response.json()['results']
        else:
            all_books = []
        return render(request, 'frontend/books.html', {
            'user': request.user,
            'books': all_books,
        })
    else:
        return redirect('login')


def book(request, book_id):
    if 'access' in request.session:
        headers = {'Authorization': f'Bearer {request.session["access"]}'}
        try:
            response = requests.get(f'http://localhost:8000/api/library/books/{book_id}/', headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logout(request)
            return render(request, 'frontend/error.html', {
                'message': 'An error occurred while fetching the book.'
            })

        if response.status_code == 200:
            book_detail = response.json()
        else:
            book_detail = {}
        return render(request, 'frontend/book.html', {
            'user': request.user,
            'book': book_detail,
        })
    else:
        return redirect('login')
