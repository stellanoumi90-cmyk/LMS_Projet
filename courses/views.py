from django.shortcuts import render
from .models import Course

def list_courses(request):
    # On récupère tous les cours de ton niveau Informatique L2
    cours_liste = Course.objects.all().order_by('code')
    return render(request, 'courses/gestion_cours.html', {'cours_liste': cours_liste})
