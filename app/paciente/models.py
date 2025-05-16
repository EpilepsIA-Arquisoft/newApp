from django.db import models
from user.models import User

class Paciente(models.Model):
    id = models.CharField(primary_key=True, max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField(default=0)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    REQUIRED_FIELDS = ['id', 'nombre', 'edad', 'doctor']

    def __str__(self):
        return self.id
