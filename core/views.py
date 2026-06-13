from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import course
from .models import Certificat
from .models import NoteEtudiant

# 1. Protection de la page d'accueil (Espace LMS)
@login_required(login_url='login')
def home(request):
    tous_les_cours = course.objects.all()
    return render(request, 'home.html', {'cours': tous_les_cours})

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

# # 3. Vue pour l'affichage de la gestion des cours (Modifiée pour le Prof)
def courses_view(request):
    # On récupère tous les cours enregistrés en base de données
    tous_les_cours = course.objects.all()
    # On les envoie au template pour qu'ils s'affichent dynamiquement
    return render(request, 'courses/gestion_cours.html', {'cours': tous_les_cours})

# # 4. Nouvelle vue pour afficher les leçons, PDF et vidéos d'un cours cliqué
from django.shortcuts import get_object_or_404
from .models import Lecon

def detail_cours(request, cours_id):
    # Récupère le cours sélectionné ou renvoie une erreur 404 s'il n'existe pas
    cours_selectionne = get_object_or_404(course, id=cours_id)
    # Récupère toutes les leçons (leçons PDF / Vidéos) liées à ce cours précis
    les_lecons = Lecon.objects.filter(cours=cours_selectionne)
    # On cherche si un certificat a été généré pour cet étudiant et ce cours
    certificat_etudiant = Certificat.objects.filter(etudiant=request.user, cours=cours_selectionne).first()
    
    return render(request, 'detail_cours.html', {
        'cours': cours_selectionne,
        'lecons': les_lecons,
        'certificat': certificat_etudiant
    })  
    
def afficher_certificat(request, certificat_id):
    # On récupère le certificat s'il appartient bien à l'étudiant connecté
     certificat = get_object_or_404(Certificat, id=certificat_id, etudiant=request.user)
     return render(request, 'certificat_template.html', {'certificat': certificat})  
     
def suivi_notes_view(request):
    # On récupère toutes les notes de l'étudiant actuellement connecté
    mes_notes = NoteEtudiant.objects.filter(etudiant=request.user)
    return render(request, 'suivi_notes.html', {'notes': mes_notes})    
   
      
