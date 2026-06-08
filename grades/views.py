from django.shortcuts import render
from .models import Grade

def student_grades(request):
    mes_notes = Grade.objects.all()
    
    # Calcul d'une petite moyenne générale de la promo pour aider l'étudiant
    total_scores = sum(note.score for note in mes_notes)
    moyenne = total_scores / mes_notes.count() if mes_notes.count() > 0 else 0

    context = {
        'mes_notes': mes_notes,
        'moyenne': round(moyenne, 2)
    }
    return render(request, 'grades/mes_notes.html', context)
