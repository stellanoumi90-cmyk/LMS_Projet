from django.db import models
from students.models import Student  # Importation de ton modèle Étudiant
from courses.models import Course    # Importation de ton modèle Cours

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Étudiant")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Matière / UE")
    score = models.FloatField(verbose_name="Note / 20")
    date_evaluation = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.course.code} : {self.score}/20"
