from django.urls import path
from .views import quiz_list, take_quiz

urlpatterns = [
    path('', quiz_list, name='quiz_list'),
    path('<int:quiz_id>/', take_quiz, name='take_quiz'),
]
