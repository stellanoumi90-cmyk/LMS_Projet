from django.db import models
from courses.models import Course

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Matière")
    title = models.CharField(max_length=200, verbose_name="Titre du Quiz")
    description = models.TextField(blank=True, verbose_name="Description")

    def __str__(self):
        return f"{self.title} ({self.course.code})"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', verbose_name="Quiz")
    text = models.TextField(verbose_name="Énoncé de la question")

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', verbose_name="Question")
    text = models.CharField(max_length=255, verbose_name="Option de réponse")
    is_correct = models.BooleanField(default=False, verbose_name="Est-ce la bonne réponse ?")

    def __str__(self):
        return self.text
