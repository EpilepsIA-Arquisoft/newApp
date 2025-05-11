from django.db import models
from paciente.models import Paciente
from resultado.models import Resultado
from datetime import date

# Lista de tipos posibles para el examen
TIPO_EXAMEN_CHOICES = [
    ('EEG','Electroencefalograma'),
]

class Examen(models.Model):
    fecha = models.DateField(default=date.today)
    tipo = models.CharField(max_length=100, choices=TIPO_EXAMEN_CHOICES)
    archivo = models.FileField(upload_to='examenes/', null=True, blank=True)
    url = models.URLField()
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    resultado = models.ForeignKey(Resultado, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.id
