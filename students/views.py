from django.shortcuts import render, redirect
from .models import Student

def gestion_etudiants(request):
    # Si le formulaire est soumis (Ajout d'un étudiant)
    if request.method == 'POST':
        matricule = request.POST.get('matricule')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        # Sauvegarde dans la base de données
        if matricule and first_name and last_name and email:
            Student.objects.create(
                matricule=matricule,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            return redirect('gestion_etudiants') # Recharge la page pour actualiser

    # Récupérer tous les étudiants pour les afficher
    etudiants = Student.objects.all()
    return render(request, 'students/gestion.html', {'etudiants': etudiants})
