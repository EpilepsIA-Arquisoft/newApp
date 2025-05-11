from datetime import date
from django.db import models
from doctor.models import Doctor
from examen.models import Examen

class Solicitud(models.Model):
    fecha = models.DateField(default=date.today)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
