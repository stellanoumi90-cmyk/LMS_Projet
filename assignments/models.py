from django.db import models
from students.models import Student
from courses.models import Course

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Matière")
    title = models.CharField(max_length=200, verbose_name="Titre du devoir")
    description = models.TextField(verbose_name="Instructions / Énoncé")
    due_date = models.DateTimeField(verbose_name="Date limite de rendu")

    def __str__(self):
        return f"{self.title} ({self.course.code})"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name="Devoir")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Étudiant")
    file_submitted = models.FileField(upload_to='devoirs_rendus/', verbose_name="Fichier rendu")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Déposé le")

    def __str__(self):
        return f"Rendu de {self.student.nom} pour {self.assignment.title}"
