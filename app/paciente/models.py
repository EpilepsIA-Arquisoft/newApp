from django.db import models

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField(default=0)

    def __str__(self):
        return self.id
