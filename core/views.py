from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

# 1. Protection de la page d'accueil (Espace LMS)
@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

# 2. Gestion de la connexion (Accepte le Nom d'utilisateur OU l'Adresse Email)
def login_view(request):
    # Si l'étudiant est déjà connecté, on l'envoie directement sur l'accueil du LMS
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        login_input = request.POST.get('username') 
        password_input = request.POST.get('password')
        
        username = login_input
        
        # Vérification si l'étudiant a entré une adresse email (présence du @)
        if login_input and '@' in login_input:
            try:
                # On récupère le nom d'utilisateur lié à cette adresse email
                user_obj = User.objects.get(email=login_input)
                username = user_obj.username
            except User.DoesNotExist:
                username = None # L'email n'existe pas dans la base de données

        # Authentification sécurisée de Django
        user = authenticate(username=username, password=password_input)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Nom d'utilisateur/Email ou mot de passe incorrect.")
            
    return render(request, 'login.html')

# 3. Vue pour l'affichage de la gestion des cours
def courses_view(request):
    return render(request, 'gestion_cours.html')    
