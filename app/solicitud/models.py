from django.db import models
from datetime import date
import uuid
from user.models import User
from examen.models import Examen

TIPO_SOLICITUD_CHOICES = [
    ('rev', 'revisión de picos'),
]

class Solicitud(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=50,
        unique=True,
        default=uuid.uuid4(),
        editable=False
    )
    fecha = models.DateField(default=date.today)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100, choices=TIPO_SOLICITUD_CHOICES, default='rev')

    def __str__(self):
        return str(self.id)
