from django.db import models

class Doctor(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.id
