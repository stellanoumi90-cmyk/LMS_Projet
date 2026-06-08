from django.urls import path
from .views import student_grades

urlpatterns = [
    path('mes-notes/', student_grades, name='student_grades'),
]
