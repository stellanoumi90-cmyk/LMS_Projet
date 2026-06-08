from django.contrib import admin
from .models import Grade

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'score', 'date_evaluation')
    list_filter = ('course', 'score')
    search_fields = ('student__nom', 'course__title')
