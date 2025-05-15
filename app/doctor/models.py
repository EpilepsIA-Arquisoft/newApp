from django.contrib.auth.models import AbstractBaseUser

from django.db import models

from user.models import User

class Doctor(AbstractBaseUser):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    #nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.id

