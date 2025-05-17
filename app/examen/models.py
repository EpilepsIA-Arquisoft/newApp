import os
from django.db import models
from paciente.models import Paciente
from resultado.models import Resultado
from datetime import date
import uuid

from bucket_upload.upload import upload

# Lista de tipos posibles para el examen
TIPO_EXAMEN_CHOICES = [
    ('EEG','Electroencefalograma'),
]

class Examen(models.Model):
    id = models.CharField(primary_key=True, max_length=50, unique=True, default=uuid.uuid4, editable=False)
    fecha = models.DateField(default=date.today)
    tipo = models.CharField(max_length=100, choices=TIPO_EXAMEN_CHOICES)
    archivo = models.FileField(upload_to='examenes_temp/')
    url = models.URLField(null=True, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    resultado = models.ForeignKey(Resultado, on_delete=models.CASCADE, null=True, blank=True)
    
    REQUIRED_FIELDS = ['id', 'tipo', 'archivo', 'paciente']

    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        try:
            subir_archivo = self.archivo and not self.url

            super().save(*args, **kwargs)

            if subir_archivo:
                # Obtén la ruta local del archivo subido
                local_path = self.archivo.path
                destination_blob_name = f"completos/examen_{self.id}.edf"

                # Llama a la función que sube el archivo al bucket
                upload(
                    self.id,
                    local_path,
                    destination_blob_name
                )

                public_url = f"https://storage.googleapis.com/examenes-eeg/{destination_blob_name}"

                # Actualiza el campo urlAcceso y guarda de nuevo el objeto
                self.url = public_url
                super().save(update_fields=["url"])
            else:
                # Si el archivo ya existe, solo actualiza la URL
                raise Exception("xd")
        except Exception as e:
            print(f"Error al subir el archivo: {e}")
            self.delete()
            raise e
        

