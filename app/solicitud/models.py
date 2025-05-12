from datetime import date
from django.db import models
from doctor.models import Doctor
from examen.models import Examen
from rabbit_writer.writer import publish_message

TIPO_SOLICITUD_CHOICES = [
    ('rev','revision de picos'),
]
class Solicitud(models.Model):
    fecha = models.DateField(default=date.today)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100, choices=TIPO_SOLICITUD_CHOICES)

    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        # Llamar a la función externa antes de guardar el objeto
        publish_message('map_requests',{
            "id_paciente": self.examen.paciente.id,
            "id_examen": self.examen.id,
            "ubicacion_examen": self.examen.url,
        })
        super().save(*args, **kwargs)
