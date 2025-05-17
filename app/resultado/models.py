from datetime import date
from django.db import models
import uuid


class Resultado(models.Model):
    id = models.CharField(primary_key=True, max_length=50, unique=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(default=date.today)
    respuesta = models.TextField()
    
    REQUIRED_FIELDS = ['id', 'respuesta']

    def __str__(self):
        return self.id
