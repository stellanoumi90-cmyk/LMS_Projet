from django.urls import path
from . import views

urlpatterns = [
    path('gestion/', views.gestion_etudiants, name='gestion_etudiants'),
]
