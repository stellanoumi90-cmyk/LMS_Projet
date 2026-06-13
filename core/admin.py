from django.contrib import admin
from .models import Profile, course, Lecon, Evaluation, NoteEtudiant, Certificat

# Configuration de l'affichage du profil (Promoteur, Enseignant, Étudiant)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)

# Configuration de l'affichage des cours
@admin.register(course)
class courseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'enseignant')
    search_fields = ('code', 'name')

# Configuration de l'affichage des leçons
@admin.register(Lecon)
class LeconAdmin(admin.ModelAdmin):
    list_display = ('titre', 'cours', 'document_pdf', 'lien_video')
    list_filter = ('cours',)

# Configuration de l'affichage des évaluations
@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'lecon', 'note_maximale')

# Configuration de l'affichage des notes et pourcentages
@admin.register(NoteEtudiant)
class NoteEtudiantAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'evaluation', 'note_obtenue', 'pourcentage_reussite_affiche', 'date_passage')
    list_filter = ('evaluation__lecon__cours', 'etudiant')

    def pourcentage_reussite_affiche(self, obj):
        return f"{obj.pourcentage_reussite():.2f} %"
    pourcentage_reussite_affiche.short_description = 'Progression (%)'
@admin.register(Certificat)
class CertificatAdmin(admin.ModelAdmin):
    list_display = ('code_verification', 'etudiant', 'cours', 'date_delivrance')
    search_fields = ('code_verification', 'etudiant__username', 'cours__name')
    
    # Empêche de créer un certificat manuellement par erreur si l'étudiant n'a pas le niveau
    def save_model(self, request, obj, form, change):
        # On récupère toutes les évaluations du cours
        total_evaluations = Evaluation.objects.filter(lecon__cours=obj.cours).count()
        # On regarde combien de notes l'étudiant a obtenues pour ce cours
        notes_etudiant = NoteEtudiant.objects.filter(etudiant=obj.etudiant, evaluation__lecon__cours=obj.cours)
        
        if notes_etudiant.count() < total_evaluations:
            from django.contrib import messages
            messages.error(request, f"Impossible de délivrer le certificat : {obj.etudiant.username} n'a pas encore passé toutes les évaluations de ce module.")
            return
            
        # Calcul de la moyenne globale en %
        total_pourcentage = sum(note.pourcentage_reussite() for note in notes_etudiant)
        moyenne_globale = total_pourcentage / total_evaluations if total_evaluations > 0 else 0
        
        if moyenne_globale >= 50.0: # Condition de validation : 50% de réussite minimum
            super().save_model(request, obj, form, change)
        else:
            from django.contrib import messages
            messages.error(request, f"Délivrance refusée : La moyenne de l'étudiant est de {moyenne_globale:.2f}%, ce qui est inférieur aux 50% requis.")
