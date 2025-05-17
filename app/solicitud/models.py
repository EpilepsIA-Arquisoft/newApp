from datetime import date
from django.db import models
from requests import Response
from user.models import User
from examen.models import Examen
from rest_framework import status
import uuid


TIPO_SOLICITUD_CHOICES = [
    ('rev','revision de picos'),
]
class Solicitud(models.Model):
    id = models.CharField(primary_key=True, max_length=50, unique=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(default=date.today)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100, choices=TIPO_SOLICITUD_CHOICES, default='rev')

    REQUIRED_FIELDS = ['id', 'doctor', 'examen', 'tipo']
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        # Llamar a la función externa antes de guardar el objeto
        try:
            if self.doctor!=self.examen.paciente.doctor:
                return Response({"detail": "No tienes permiso para ver este examen."}, status=status.HTTP_403_FORBIDDEN)
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

