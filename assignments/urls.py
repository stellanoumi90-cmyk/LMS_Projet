from django.urls import path
from .views import list_assignments

urlpatterns = [
    path('espace/', list_assignments, name='list_assignments'),
]
