from django.urls import path
from . import views

urlpatterns = [
    path('gestion/', views.list_courses, name='list_courses'),
]
