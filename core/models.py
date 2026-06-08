from django.db import models

class course(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
