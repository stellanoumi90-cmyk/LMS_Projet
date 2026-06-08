from django.shortcuts import render, redirect, get_object_or_404
from .models import Assignment, Submission
from students.models import Student

def list_assignments(request):
    devoirs = Assignment.objects.all()
    
    if request.method == 'POST':
        assignment_id = request.POST.get('assignment_id')
        fichier = request.FILES.get('devoir_file')
        
        # Pour le test, on prend le premier étudiant de la base de données
        # Plus tard, ce sera l'étudiant connecté (request.user)
        etudiant = Student.objects.first() 
        devoir = Assignment.objects.get(id=assignment_id)
        
        if fichier and etudiant:
            Submission.objects.create(
                assignment=devoir,
                student=etudiant,
                file_submitted=fichier
            )
            return redirect('list_assignments')

    return render(request, 'assignments/espace_devoirs.html', {'devoirs': devoirs})
