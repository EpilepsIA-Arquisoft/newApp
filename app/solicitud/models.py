from datetime import date
from django.db import models
from user.models import User
from examen.models import Examen


TIPO_SOLICITUD_CHOICES = [
    ('rev','revision de picos'),
]
class Solicitud(models.Model):
    fecha = models.DateField(default=date.today)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100, choices=TIPO_SOLICITUD_CHOICES, default='rev')

    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        # Llamar a la función externa antes de guardar el objeto
        try:
            msj = {
                "id_paciente": self.examen.paciente.id,
                "id_examen": self.examen.id,
                "ubicacion_examen": self.examen.url,
            }
            #from rabbit_writer.writer import publish_message
            #publish_message('map_requests',msj)
            super().save(*args, **kwargs)
        except Exception as e:
            print(f"Error al publicar el mensaje: {e}")

