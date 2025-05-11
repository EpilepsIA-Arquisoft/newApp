from datetime import date
from django.db import models

class Resultado(models.Model):
    fecha = models.DateField(default=date.today)
    respuesta = models.TextField()

    def __str__(self):
        return self.id
