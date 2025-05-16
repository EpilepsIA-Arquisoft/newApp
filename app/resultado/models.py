from datetime import date
from django.db import models

class Resultado(models.Model):
    id = models.CharField(primary_key=True, max_length=50, unique=True)
    fecha = models.DateField(default=date.today)
    respuesta = models.TextField()
    
    REQUIRED_FIELDS = ['id', 'respuesta']

    def __str__(self):
        return self.id
