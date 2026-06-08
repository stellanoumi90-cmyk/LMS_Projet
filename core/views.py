from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login

def home(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')
    
def courses_view(request):
    return render(request, 'courses.html')    
