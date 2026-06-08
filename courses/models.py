from django.db import models

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)  # Ex: INF222, INF212
    title = models.CharField(max_length=200)             # Ex: Base de données
    description = models.TextField(blank=True, null=True)
    support_pdf = models.FileField(upload_to='cours_pdf/', blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.title}"
